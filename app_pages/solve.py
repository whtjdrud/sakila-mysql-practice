import pymysql
import streamlit as st

from app_state import (filtered_problems, load_progress, mark_solved, problem_by_id,
                       solution_result, table_columns)
from sakila_bank import grade, level_label, run_query

by_id = problem_by_id()
solved = load_progress()

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

left, right = st.columns([1, 1], gap="large")

with left:
    tab_q, tab_schema = st.tabs(["문제", "테이블 구조"])
    with tab_q:
        st.markdown(prob["question"])
    with tab_schema:
        if not prob["tables"]:
            st.caption("이 문제는 테이블을 사용하지 않습니다.")
        try:
            cols = table_columns(tuple(prob["tables"]))
            for t in prob["tables"]:
                with st.expander(t, icon=":material/table:"):
                    st.dataframe(cols[cols["테이블"] == t].drop(columns="테이블"), hide_index=True)
        except pymysql.MySQLError as e:
            st.error(f"DB 연결 실패: {e}")

with right:
    sql = st.text_area("SQL 작성", key=f"sql_{pid}", height=280,
                       placeholder="SELECT ...", label_visibility="collapsed")
    with st.container(horizontal=True):
        run_clicked = st.button("실행", icon=":material/play_arrow:")
        submit_clicked = st.button("제출(채점)", type="primary", icon=":material/check:")
        reveal = st.toggle("정답·해설 보기", key=f"reveal_{pid}")

    out_key = f"out_{pid}"
    if (run_clicked or submit_clicked) and not sql.strip():
        st.session_state[out_key] = {"status": "warning", "msg": "SQL 을 입력하세요."}
    elif run_clicked or submit_clicked:
        try:
            result = run_query(sql)
            out = {"df": result}
            if submit_clicked:
                out["status"], out["msg"] = grade(result, solution_result(prob["solution"]),
                                                  prob["ordered"])
            st.session_state[out_key] = out
            # 처음 맞힌 경우 진행률·해설까지 갱신되도록 다시 그린다
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
