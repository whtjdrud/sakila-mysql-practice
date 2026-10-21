"""문제 은행 공통 모듈 (빌드 스크립트와 웹앱이 함께 사용)

bank/<유형코드>.yaml 에 문제를 리스트로 작성한다.

- id: SUB-001             # 유형코드-번호 (고정, 바꾸지 말 것)
  title: 제목
  level: 3                # 1 입문 ~ 5 최고급
  tags: [IN, 스칼라 서브쿼리]
  question: |             # 문제 설명 (마크다운)
  solution: |             # 정답 쿼리 (결과를 반환하는 문장 1개)
  note: |                 # 해설 (마크다운)
  ordered: false          # (선택) 행 순서를 채점하지 않을 때
"""

from pathlib import Path

import pandas as pd
import pymysql
import yaml

ROOT = Path(__file__).resolve().parent
BANK = ROOT / "bank"
DB = dict(host="127.0.0.1", port=3307, user="learner", password="learner",
          database="sakila", charset="utf8mb4")
TIMEOUT_MS = 10_000

# (코드, 폴더명, 이름, 설명)
CATEGORIES = [
    ("SEL", "01-basic-select", "기본 조회", "SELECT · WHERE · ORDER BY · LIMIT · DISTINCT"),
    ("FN", "02-functions", "함수", "문자열 · 숫자 · 날짜 함수, NULL 처리"),
    ("AGG", "03-aggregate", "집계", "집계 함수 · GROUP BY · HAVING · ROLLUP"),
    ("JOIN", "04-join", "조인", "INNER · LEFT · SELF · 다중 조인 · 안티 조인"),
    ("SUB", "05-subquery", "서브쿼리", "스칼라 · IN · EXISTS · 상관 · 파생 테이블"),
    ("CASE", "06-case-set", "조건식·집합", "CASE · 피벗 · UNION · 집합 연산"),
    ("CTE", "07-cte", "CTE", "WITH · 다단계 CTE · 재귀 CTE"),
    ("WIN", "08-window", "윈도우 함수", "순위 · 누적 · 이동 평균 · LAG/LEAD"),
    ("ADV", "09-advanced", "복합 분석", "코호트 · 리텐션 · 갭/섬 · 실무형 리포트"),
]
CATEGORY_BY_CODE = {c[0]: c for c in CATEGORIES}

LEVELS = {1: "입문", 2: "초급", 3: "중급", 4: "고급", 5: "최고급"}


def level_label(level: int) -> str:
    return f"{'★' * level}{'☆' * (5 - level)} {LEVELS[level]}"


def load_bank() -> list[dict]:
    """모든 문제를 유형 순서 → id 순서로 돌려준다."""
    problems = []
    for code, folder, name, _ in CATEGORIES:
        path = BANK / f"{code}.yaml"
        if not path.exists():
            continue
        for p in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
            p["category"] = code
            p["category_name"] = name
            p["folder"] = folder
            # YAML 은 태그 NULL 을 None 으로 읽으므로 문자열로 되돌린다
            p["tags"] = ["NULL" if t is None else str(t) for t in p.get("tags") or []]
            p["solution"] = p["solution"].strip()
            p["question"] = p["question"].strip()
            p["note"] = (p.get("note") or "").strip()
            p["ordered"] = p.get("ordered", "ORDER BY" in p["solution"].upper())
            problems.append(p)
    return problems


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
            return pd.DataFrame(list(cur.fetchall()), columns=cols)
    finally:
        conn.close()


def _cell(v) -> str:
    if v is None:
        return "NULL"
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return str(v)


def normalize(df: pd.DataFrame) -> list[tuple]:
    """값 비교용: 모든 값을 문자열로 (숫자는 소수 둘째 자리까지)"""
    return [tuple(_cell(v) for v in row) for row in df.itertuples(index=False)]


def grade(user: pd.DataFrame, answer: pd.DataFrame, ordered: bool) -> tuple[str, str]:
    """(상태, 메시지) — 상태는 success / warning / error"""
    if user.shape[1] != answer.shape[1]:
        return "error", f"컬럼 수가 다릅니다. (내 답 {user.shape[1]}개, 정답 {answer.shape[1]}개)"
    if len(user) != len(answer):
        return "error", f"행 수가 다릅니다. (내 답 {len(user)}행, 정답 {len(answer)}행)"
    u, a = normalize(user), normalize(answer)
    same_values = u == a if ordered else sorted(u) == sorted(a)
    if same_values:
        if [c.lower() for c in user.columns] != [c.lower() for c in answer.columns]:
            return "success", "정답입니다! (컬럼 이름이 문제에서 요구한 별칭과 다르니 확인해 보세요)"
        return "success", "정답입니다!"
    if sorted(u) == sorted(a):
        return "warning", "결과 값은 맞지만 정렬 순서가 다릅니다. ORDER BY 조건을 확인하세요."
    return "error", "결과 값이 정답과 다릅니다."
