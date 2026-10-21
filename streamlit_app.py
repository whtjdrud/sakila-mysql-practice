"""Sakila SQL 연습 웹앱

실행: streamlit run streamlit_app.py
problems/ 폴더의 문제를 불러와 브라우저에서 SQL 을 작성·실행하고,
정답 쿼리 결과와 비교해 채점한다.
"""

import json
import re
from pathlib import Path

import pandas as pd
import pymysql
import streamlit as st

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"
PROGRESS_FILE = ROOT / "progress.json"  # 푼 문제 기록 (git 제외)
DB = dict(host="127.0.0.1", port=3307, user="learner", password="learner",
          database="sakila", charset="utf8mb4")
TIMEOUT_MS = 10_000

st.set_page_config(page_title="Sakila SQL 연습", page_icon=":material/database:",
                   layout="wide")


# ---------- 데이터 로딩 ----------

@st.cache_data
def load_problems() -> list[dict]:
    items = []
    for d in sorted(p for p in PROBLEMS.iterdir() if p.is_dir()):
        text = (d / "problem.md").read_text(encoding="utf-8")
        title = re.search(r"^#\s+(.+)$", text, re.M)
        level = re.search(r"^level:\s*(.+)$", text, re.M | re.I)
        body = re.sub(r"^level:.*\n?", "", text, flags=re.M | re.I)
        body = re.sub(r"^#\s+.+\n?", "", body, count=1, flags=re.M).strip()
        tables = re.search(r"\*\*사용 테이블:\*\*\s*(.+)$", text, re.M)
        analysis = d / "analysis.md"
        items.append({
            "id": d.name[:3],
            "title": title.group(1).strip() if title else d.name,
            "level": level.group(1).strip() if level else "-",
            "body": body,
            "tables": re.findall(r"`(\w+)`", tables.group(1)) if tables else [],
            "solution": (d / "solution.sql").read_text(encoding="utf-8").strip(),
            "analysis": analysis.read_text(encoding="utf-8") if analysis.exists() else "",
        })
    return items


def run_query(sql: str) -> pd.DataFrame:
    """읽기 전용 계정으로 쿼리 1개를 실행해 DataFrame 으로 돌려준다."""
    sql = sql.strip().rstrip(";").strip()
    conn = pymysql.connect(**DB, read_timeout=TIMEOUT_MS // 1000 + 5)
    try:
        with conn.cursor() as cur:
            cur.execute(f"SET SESSION MAX_EXECUTION_TIME = {TIMEOUT_MS}")
            cur.execute(sql)
            if cur.description is None:
                return pd.DataFrame()
            cols = [c[0] for c in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=cols)
    finally:
        conn.close()


@st.cache_data
def solution_result(sql: str) -> pd.DataFrame:
    return run_query(sql)


@st.cache_data
def table_columns(tables: tuple[str, ...]) -> pd.DataFrame:
    if not tables:
        return pd.DataFrame()
    marks = ",".join(["%s"] * len(tables))
    conn = pymysql.connect(**DB)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""SELECT table_name, column_name, column_type, column_key
                    FROM information_schema.columns
                    WHERE table_schema = 'sakila' AND table_name IN ({marks})
                    ORDER BY FIELD(table_name, {marks}), ordinal_position""",
                tables + tables)
            return pd.DataFrame(cur.fetchall(),
                                columns=["테이블", "컬럼", "타입", "키"])
    finally:
        conn.close()


# ---------- 채점 ----------

def normalize(df: pd.DataFrame) -> list[tuple]:
    """값 비교용: 모든 값을 문자열로 (숫자는 소수 둘째 자리까지)"""
    def cell(v):
        if v is None:
            return "NULL"
        try:
            return f"{float(v):.2f}"
        except (TypeError, ValueError):
            return str(v)
    return [tuple(cell(v) for v in row) for row in df.itertuples(index=False)]


def grade(user: pd.DataFrame, answer: pd.DataFrame) -> tuple[str, str]:
    """(상태, 메시지) — 상태는 success / warning / error"""
    if user.shape[1] != answer.shape[1]:
        return "error", f"컬럼 수가 다릅니다. (내 답 {user.shape[1]}개, 정답 {answer.shape[1]}개)"
    if len(user) != len(answer):
        return "error", f"행 수가 다릅니다. (내 답 {len(user)}행, 정답 {len(answer)}행)"
    u, a = normalize(user), normalize(answer)
    if u == a:
        names_differ = [x.lower() for x in user.columns] != [x.lower() for x in answer.columns]
        if names_differ:
            return "success", "정답입니다! (컬럼 이름은 문제에서 요구한 별칭과 다르니 확인해 보세요)"
        return "success", "정답입니다!"
    if sorted(u) == sorted(a):
        return "warning", "결과 값은 맞지만 정렬 순서가 다릅니다. ORDER BY 조건을 확인하세요."
    return "error", "결과 값이 정답과 다릅니다."


# ---------- 진행 기록 ----------

def load_progress() -> set[str]:
    try:
        return set(json.loads(PROGRESS_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return set()


def mark_solved(pid: str) -> None:
    solved = load_progress() | {pid}
    PROGRESS_FILE.write_text(json.dumps(sorted(solved)), encoding="utf-8")


# ---------- 화면 ----------

problems = load_problems()
solved = load_progress()

with st.sidebar:
    st.header("Sakila SQL 연습", divider="gray")
    st.progress(len(solved & {p["id"] for p in problems}) / max(len(problems), 1),
                text=f"{len(solved)} / {len(problems)} 문제 해결")
    labels = {p["id"]: f"{p['id']}. {p['title']}{' ✅' if p['id'] in solved else ''}"
              for p in problems}
    # key 를 고정해야 ✅ 표시로 라벨이 바뀌어도 선택이 유지된다
    pid = st.radio("문제 선택", list(labels), format_func=labels.get,
                   key="problem_id", label_visibility="collapsed")
    st.caption("DB: localhost:3307 / 읽기 전용 계정(learner)")

prob = next(p for p in problems if p["id"] == pid)

st.title(f"{prob['id']}. {prob['title']}")
st.badge(prob["level"], color="blue")

left, right = st.columns([1, 1], gap="large")

with left:
    tab_q, tab_schema = st.tabs(["문제", "테이블 구조"])
    with tab_q:
        st.markdown(prob["body"])
    with tab_schema:
        try:
            cols = table_columns(tuple(prob["tables"]))
            for t in prob["tables"]:
                with st.expander(t, icon=":material/table:"):
                    st.dataframe(cols[cols["테이블"] == t].drop(columns="테이블"),
                                 hide_index=True)
        except pymysql.MySQLError as e:
            st.error(f"DB 연결 실패: {e}")

with right:
    sql = st.text_area("SQL 작성", key=f"sql_{pid}", height=260,
                       placeholder="SELECT ...", label_visibility="collapsed")
    with st.container(horizontal=True):
        run_clicked = st.button("실행", icon=":material/play_arrow:")
        submit_clicked = st.button("제출(채점)", type="primary",
                                   icon=":material/check:")
        reveal = st.toggle("정답·해설 보기", key=f"reveal_{pid}")

    out_key = f"out_{pid}"
    if (run_clicked or submit_clicked) and not sql.strip():
        st.session_state[out_key] = {"status": "warning", "msg": "SQL 을 입력하세요."}
    elif run_clicked or submit_clicked:
        try:
            result = run_query(sql)
            out = {"df": result}
            if submit_clicked:
                out["status"], out["msg"] = grade(result, solution_result(prob["solution"]))
            st.session_state[out_key] = out
            # 처음 맞힌 경우 사이드바·해설까지 갱신되도록 다시 그린다
            if out.get("status") == "success" and pid not in solved:
                mark_solved(pid)
                st.session_state["celebrate"] = True
                st.rerun()
        except pymysql.MySQLError as e:
            st.session_state[out_key] = {
                "status": "error", "msg": f"SQL 오류: {e.args[-1] if e.args else e}"}

    out = st.session_state.get(out_key)
    if out:
        if "df" in out:
            st.dataframe(out["df"], hide_index=True, height=300)
            st.caption(f"{len(out['df'])}행")
        if "status" in out:
            getattr(st, out["status"])(out["msg"])
    if st.session_state.pop("celebrate", False):
        st.balloons()

if reveal or pid in solved:
    st.divider()
    sol_tab, ana_tab, ans_tab = st.tabs(["정답 쿼리", "해설·분석", "정답 결과"])
    with sol_tab:
        st.code(prob["solution"], language="sql")
    with ana_tab:
        st.markdown(prob["analysis"] or "_(해설 없음)_")
    with ans_tab:
        try:
            st.dataframe(solution_result(prob["solution"]), hide_index=True)
        except pymysql.MySQLError as e:
            st.error(f"DB 연결 실패: {e}")
