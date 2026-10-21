import pandas as pd
import streamlit as st

from sakila_bank import run_query

st.title("스키마 탐색")
st.caption("Workbench 의 Navigator 처럼 테이블 구조를 둘러보는 곳입니다. "
           "같은 정보를 에디터에서 `SHOW TABLES;` · `DESCRIBE film;` · `SHOW CREATE TABLE film;` 으로도 얻을 수 있습니다.")


@st.cache_data
def tables() -> pd.DataFrame:
    df = run_query("""
        SELECT table_name AS 이름, table_type AS 종류, table_comment AS 설명
        FROM information_schema.tables
        WHERE table_schema = 'sakila'
        ORDER BY table_type, table_name""")
    df["종류"] = df["종류"].map({"BASE TABLE": "테이블", "VIEW": "뷰"})
    # information_schema 의 행 수는 InnoDB 추정치라 실제로 센다 (작은 DB 라 빠름)
    df["행 수"] = [int(run_query(f"SELECT COUNT(*) AS n FROM `{t}`")["n"][0]) for t in df["이름"]]
    return df


@st.cache_data
def columns(table: str) -> pd.DataFrame:
    return run_query(f"""
        SELECT column_name AS 컬럼, column_type AS 타입, is_nullable AS `NULL`,
               column_key AS 키, column_default AS 기본값, extra AS 기타
        FROM information_schema.columns
        WHERE table_schema = 'sakila' AND table_name = '{table}'
        ORDER BY ordinal_position""")


@st.cache_data
def foreign_keys() -> pd.DataFrame:
    return run_query("""
        SELECT table_name AS 테이블, column_name AS 컬럼,
               referenced_table_name AS 참조_테이블, referenced_column_name AS 참조_컬럼
        FROM information_schema.key_column_usage
        WHERE table_schema = 'sakila' AND referenced_table_name IS NOT NULL
        ORDER BY table_name, column_name""")


all_tables = tables()
fks = foreign_keys()

left, right = st.columns([1, 2], gap="large")
with left:
    kind = st.segmented_control("종류", ["전체", "테이블", "뷰"], default="전체", key="schema_kind")
    shown = all_tables if kind in (None, "전체") else all_tables[all_tables["종류"] == kind]
    names = list(shown["이름"])
    table = st.selectbox("테이블 선택", names,
                         index=names.index("film") if "film" in names else 0, key="schema_table")
    st.dataframe(shown[["이름", "종류", "행 수"]], hide_index=True)

with right:
    row = all_tables[all_tables["이름"] == table].iloc[0]
    st.subheader(table)
    st.caption(f"{row['종류']} · {row['행 수']:,}행" + (f" · {row['설명']}" if row["설명"] else ""))
    tab_cols, tab_rel, tab_sample, tab_ddl = st.tabs(["컬럼", "관계", "샘플 데이터", "DDL"])
    with tab_cols:
        st.dataframe(columns(table), hide_index=True)
        st.caption("키: PRI = 기본키, MUL = 인덱스(중복 허용), UNI = 고유 인덱스")
    with tab_rel:
        out_fk = fks[fks["테이블"] == table]
        in_fk = fks[fks["참조_테이블"] == table]
        st.markdown("**이 테이블이 참조하는 테이블** (FK →)")
        if out_fk.empty:
            st.caption("없음")
        else:
            st.dataframe(out_fk.drop(columns="테이블"), hide_index=True)
        st.markdown("**이 테이블을 참조하는 테이블** (← FK)")
        if in_fk.empty:
            st.caption("없음")
        else:
            st.dataframe(in_fk[["테이블", "컬럼", "참조_컬럼"]], hide_index=True)
        if row["종류"] == "뷰":
            st.caption("뷰는 FK 가 없습니다. DDL 탭에서 어떤 테이블을 조인하는지 확인하세요.")
    with tab_sample:
        st.dataframe(run_query(f"SELECT * FROM `{table}` LIMIT 10"), hide_index=True)
    with tab_ddl:
        ddl = run_query(f"SHOW CREATE {'VIEW' if row['종류'] == '뷰' else 'TABLE'} `{table}`")
        st.code(ddl.iloc[0, 1], language="sql")

with st.expander("전체 FK 관계 목록", icon=":material/account_tree:"):
    st.dataframe(fks, hide_index=True)
