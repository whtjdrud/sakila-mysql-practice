"""Sakila SQL 연습 웹앱

실행: streamlit run streamlit_app.py
bank/*.yaml 문제 은행을 불러와 유형·난이도별로 조회하고,
브라우저에서 SQL 을 작성·실행해 정답 쿼리 결과와 비교해 채점한다.
"""

import streamlit as st

from app_state import render_sidebar_filters

st.set_page_config(page_title="Sakila SQL 연습", page_icon=":material/database:",
                   layout="wide")

page = st.navigation([
    st.Page("app_pages/problem_list.py", title="문제 목록", icon=":material/list:", default=True),
    st.Page("app_pages/solve.py", title="문제 풀기", icon=":material/edit_note:"),
    st.Page("app_pages/schema.py", title="스키마 탐색", icon=":material/schema:"),
    st.Page("app_pages/stats.py", title="학습 통계", icon=":material/insights:"),
])

render_sidebar_filters()
page.run()
