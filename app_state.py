"""웹앱 공통 상태: 문제 은행 캐시, 풀이 기록, 사이드바 필터"""

import json
import re

import pandas as pd
import pymysql
import streamlit as st

from sakila_bank import CATEGORIES, DB, LEVELS, ROOT, load_bank, run_query

PROGRESS_FILE = ROOT / "progress.json"  # 푼 문제 기록 (git 제외)
STATUS_OPTIONS = ["전체", "안 푼 문제", "푼 문제"]


@st.cache_data
def problems() -> list[dict]:
    items = load_bank()
    for p in items:
        tables = re.search(r"\*\*사용 테이블:\*\*\s*(.+)$", p["question"], re.M)
        p["tables"] = re.findall(r"`(\w+)`", tables.group(1)) if tables else []
    return items


def problem_by_id() -> dict[str, dict]:
    return {p["id"]: p for p in problems()}


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
            return pd.DataFrame(cur.fetchall(), columns=["테이블", "컬럼", "타입", "키"])
    finally:
        conn.close()


def load_progress() -> set[str]:
    try:
        return set(json.loads(PROGRESS_FILE.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return set()


def mark_solved(pid: str) -> None:
    solved = load_progress() | {pid}
    PROGRESS_FILE.write_text(json.dumps(sorted(solved)), encoding="utf-8")


def render_sidebar_filters() -> None:
    """사이드바에 진행률과 필터를 그린다. 값은 session_state 에 남아 페이지 간에 공유된다."""
    items = problems()
    solved = load_progress()
    done = len(solved & {p["id"] for p in items})
    with st.sidebar:
        st.progress(done / max(len(items), 1), text=f"{done} / {len(items)} 문제 해결")
        st.multiselect("유형", [c[0] for c in CATEGORIES], key="f_categories",
                       format_func=lambda c: next(x[2] for x in CATEGORIES if x[0] == c),
                       placeholder="전체 유형")
        st.pills("난이도", list(LEVELS), key="f_levels", selection_mode="multi",
                 format_func=lambda l: f"{'★' * l} {LEVELS[l]}")
        st.segmented_control("풀이 상태", STATUS_OPTIONS, key="f_status", default="전체")
        st.text_input("검색", key="f_search", placeholder="제목·태그·ID (예: 윈도우, LAG, SUB-01)")
        st.caption("DB: localhost:3307 · 읽기 전용 계정(learner)")


def filtered_problems() -> list[dict]:
    solved = load_progress()
    cats = st.session_state.get("f_categories") or []
    levels = st.session_state.get("f_levels") or []
    status = st.session_state.get("f_status") or "전체"
    query = (st.session_state.get("f_search") or "").strip().lower()
    out = []
    for p in problems():
        if cats and p["category"] not in cats:
            continue
        if levels and p["level"] not in levels:
            continue
        if status == "푼 문제" and p["id"] not in solved:
            continue
        if status == "안 푼 문제" and p["id"] in solved:
            continue
        if query and query not in " ".join([p["id"], p["title"], *p["tags"]]).lower():
            continue
        out.append(p)
    return out
