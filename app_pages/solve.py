import re

import pandas as pd
import pymysql
import streamlit as st

from app_state import (filtered_problems, load_progress, problem_by_id, record_attempt,
                       record_reveal, solution_result, table_columns)
from sakila_bank import grade, level_label, run_many
from sql_editor import pick_statements, sql_editor

by_id = problem_by_id()
solved = load_progress()
practice = st.session_state.get("practice_mode", False)

# 현재 문제: URL(?pid=...) → 세션 → 필터 첫 문제 순으로 정한다
ids = [p["id"] for p in filtered_problems()] or list(by_id)
pid = st.query_params.get("pid") or st.session_state.get("pid")
if pid not in by_id:
    pid = ids[0]
# 이동 범위는 현재 필터 결과. 선택된 문제가 필터 밖이면 목록에 함께 넣어 둔다.
if pid not in ids:
    ids = [pid] + ids
st.session_state["pid"] = pid
st.query_params["pid"] = pid  # 북마크·공유할 수 있도록 URL 에 남긴다
# 선택 상자 값은 위젯 생성 전에 맞춰 둔다 (목록 페이지·이전/다음 버튼에서 온 경우)
st.session_state["pid_select"] = pid
pos = ids.index(pid)


def go(new_pid: str) -> None:
    st.session_state["pid"] = new_pid
    st.query_params["pid"] = new_pid


def on_select() -> None:
    go(st.session_state["pid_select"])


with st.container(horizontal=True, vertical_alignment="bottom"):
    st.selectbox(
        "문제 이동", ids, key="pid_select", on_change=on_select,
        format_func=lambda i: f"{'✅ ' if i in solved else ''}{i}. {by_id[i]['title']}")
    st.button("이전", icon=":material/chevron_left:", disabled=pos == 0,
              on_click=go, args=(ids[max(pos - 1, 0)],))
    st.button("다음", icon=":material/chevron_right:", disabled=pos == len(ids) - 1,
              on_click=go, args=(ids[min(pos + 1, len(ids) - 1)],))

prob = by_id[pid]
st.title(f"{prob['id']}. {prob['title']}")
with st.container(horizontal=True):
    st.badge(prob["category_name"], icon=":material/category:", color="violet")
    st.badge(level_label(prob["level"]), color="blue")
    for t in prob["tags"]:
        st.badge(t, color="gray")
    if pid in solved:
        st.badge("해결", icon=":material/check:", color="green")
    if practice:
        st.badge("실무 모드", icon=":material/work:", color="orange")

left, right = st.columns([2, 3], gap="large")

with left:
    if practice:
        st.markdown(re.sub(r"\n*\*\*사용 테이블:\*\*.*$", "", prob["question"], flags=re.M))
        st.caption("실무 모드: 필요한 테이블을 직접 찾아보세요. "
                   "`SHOW TABLES;` · `DESCRIBE 테이블;` 를 실행하거나 **스키마 탐색** 페이지를 이용할 수 있습니다.")
    else:
        tab_q, tab_schema = st.tabs(["문제", "테이블 구조"])
        with tab_q:
            st.markdown(prob["question"])
        with tab_schema:
            if not prob["tables"]:
                st.caption("이 문제에는 테이블 힌트가 없습니다. 문제의 쿼리를 참고하거나 스키마 탐색 페이지를 이용하세요.")
            try:
                cols = table_columns(tuple(prob["tables"]))
                for t in prob["tables"]:
                    with st.expander(t, icon=":material/table:"):
                        st.dataframe(cols[cols["테이블"] == t].drop(columns="테이블"), hide_index=True)
            except pymysql.MySQLError as e:
                st.error(f"DB 연결 실패: {e}")

with right:
    texts = st.session_state.setdefault("sql_texts", {})
    run, saved = sql_editor(key=f"editor_{pid}", value=texts.get(pid, ""))
    if saved is not None:
        texts[pid] = saved
    st.caption("여러 문장을 써 두고 원하는 부분만 선택해 Ctrl+Enter 로 실행할 수 있습니다. "
               "제출은 선택 영역(없으면 커서 위치 문장)의 마지막 결과로 채점합니다.")

    out_key = f"out_{pid}"
    if run:
        texts[pid] = run["text"]
        stmts = pick_statements(run["text"], run["sel_start"], run["sel_end"], run["action"])
        if not stmts:
            st.session_state[out_key] = {"status": "warning", "msg": "실행할 SQL 이 없습니다."}
        else:
            try:
                results = run_many(stmts)
            except pymysql.MySQLError as e:
                results = [{"sql": stmts[0], "error": str(e), "sec": 0}]
            out = {"results": results}
            if run["action"] == "submit":
                failed = next((r for r in results if "error" in r), None)
                answer_df = next((r["df"] for r in reversed(results) if "df" in r), None)
                if failed:
                    out["status"], out["msg"] = "error", f"SQL 오류: {failed['error']}"
                    record_attempt(pid, "sql_error")
                elif answer_df is None:
                    out["status"], out["msg"] = "warning", "채점할 결과셋(SELECT 결과)이 없습니다."
                else:
                    out["status"], out["msg"] = grade(answer_df, solution_result(prob["solution"]),
                                                      prob["ordered"])
                    record_attempt(pid, out["status"])
            st.session_state[out_key] = out
            # 처음 맞힌 경우 진행률·해설까지 갱신되도록 다시 그린다
            if out.get("status") == "success" and pid not in solved:
                st.session_state["celebrate"] = True
                st.rerun()

    out = st.session_state.get(out_key)
    if out:
        results = out.get("results", [])
        sets = [r for r in results if "df" in r]
        if len(results) > 1:
            log = pd.DataFrame([{
                "#": i + 1,
                "문장": r["sql"].replace("\n", " ")[:80],
                "결과": r["error"] if "error" in r else
                        f"{len(r['df'])}행" if "df" in r else f"{r.get('rowcount', 0)}행 영향",
                "시간(초)": round(r["sec"], 3),
            } for i, r in enumerate(results)])
            st.dataframe(log, hide_index=True)
        if len(sets) == 1:
            st.dataframe(sets[0]["df"], hide_index=True)
            st.caption(f"{len(sets[0]['df'])}행 · {sets[0]['sec']:.3f}초")
        elif sets:
            for tab, r in zip(st.tabs([f"결과 {i + 1}" for i in range(len(sets))]), sets):
                with tab:
                    st.dataframe(r["df"], hide_index=True)
                    st.caption(f"{len(r['df'])}행 · {r['sec']:.3f}초")
        if len(results) == 1 and "error" in results[0]:
            st.error(f"SQL 오류: {results[0]['error']}")
        if "status" in out:
            getattr(st, out["status"])(out["msg"])
    if st.session_state.pop("celebrate", False):
        st.balloons()

    reveal = st.toggle("정답·해설 보기", key=f"reveal_{pid}",
                       on_change=lambda: st.session_state.get(f"reveal_{pid}") and record_reveal(pid))

if reveal or pid in solved:
    st.divider()
    sol_tab, note_tab, ans_tab = st.tabs(["정답 쿼리", "해설", "정답 결과"])
    with sol_tab:
        st.code(prob["solution"], language="sql")
    with note_tab:
        st.markdown(prob["note"] or "_(해설 없음)_")
    with ans_tab:
        try:
            st.dataframe(solution_result(prob["solution"]), hide_index=True)
        except pymysql.MySQLError as e:
            st.error(f"DB 연결 실패: {e}")
