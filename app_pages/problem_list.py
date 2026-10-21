import pandas as pd
import streamlit as st

from app_state import filtered_problems, load_progress, problems
from sakila_bank import CATEGORIES, LEVELS

items = filtered_problems()
solved = load_progress()

st.title("문제 목록")

with st.container(horizontal=True):
    st.metric("전체 문제", len(problems()), border=True)
    st.metric("필터 결과", len(items), border=True)
    st.metric("해결", len(solved & {p["id"] for p in problems()}), border=True)

with st.expander("유형 × 난이도 현황", icon=":material/grid_view:"):
    matrix = pd.DataFrame(
        [[sum(1 for p in problems() if p["category"] == code and p["level"] == lv)
          for lv in LEVELS] for code, *_ in CATEGORIES],
        index=[f"{name} ({code})" for code, _, name, _ in CATEGORIES],
        columns=[LEVELS[lv] for lv in LEVELS])
    matrix["합계"] = matrix.sum(axis=1)
    st.dataframe(matrix)

if not items:
    st.info("조건에 맞는 문제가 없습니다. 사이드바 필터를 조정해 보세요.")
    st.stop()

table = pd.DataFrame([{
    "상태": "✅" if p["id"] in solved else "",
    "ID": p["id"],
    "유형": p["category_name"],
    "제목": p["title"],
    "난이도": "★" * p["level"],
    "태그": ", ".join(p["tags"]),
} for p in items])

st.caption("행을 클릭하면 풀이 화면으로 이동합니다.")
event = st.dataframe(
    table, hide_index=True, on_select="rerun", selection_mode="single-row",
    height=min(38 + 35 * len(table), 640),
    column_config={
        "상태": st.column_config.TextColumn(width="small"),
        "ID": st.column_config.TextColumn(width="small"),
        "난이도": st.column_config.TextColumn(width="small"),
    })

if event.selection.rows:
    pid = table.iloc[event.selection.rows[0]]["ID"]
    st.session_state["pid"] = pid
    st.switch_page("app_pages/solve.py", query_params={"pid": pid})
