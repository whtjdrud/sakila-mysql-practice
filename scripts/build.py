"""Sakila 문제 빌드 스크립트

problems/<번호-슬러그>/ 폴더마다
  - problem.md   : 문제 설명 (첫 줄 '# 제목', 'level:' 줄로 난이도 표기)
  - solution.sql : 정답 쿼리 (여러 문장이면 마지막 SELECT 결과만 기록)
  - analysis.md  : 풀이 해설/분석
를 읽어 solution.sql 을 Docker 의 MySQL 에서 실행하고,
결과표를 포함한 README.md 를 생성한다. 루트 README.md 의 목록도 갱신한다.

사용법:
  python scripts/build.py            # 전체 빌드
  python scripts/build.py 003        # 특정 번호만 빌드
  python scripts/build.py --push     # 빌드 후 git commit & push
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
CONTAINER = "sakila-mysql"
MYSQL_CMD = ["docker", "exec", "-i", CONTAINER, "mysql", "-uroot", "-psakila",
             "--default-character-set=utf8mb4", "--batch", "sakila"]
MAX_ROWS = 20  # README 에 표시할 최대 행 수


def run_sql(sql: str) -> tuple[list[str], list[list[str]]]:
    """SQL 을 실행하고 (컬럼명, 행 목록) 을 돌려준다."""
    proc = subprocess.run(MYSQL_CMD, input=sql.encode("utf-8"),
                          capture_output=True)
    stderr = proc.stderr.decode("utf-8", "replace")
    # 비밀번호 경고는 무시
    errors = [l for l in stderr.splitlines() if "Using a password" not in l]
    if proc.returncode != 0 or errors:
        raise RuntimeError("\n".join(errors) or f"exit {proc.returncode}")
    lines = proc.stdout.decode("utf-8", "replace").rstrip("\n").split("\n")
    if not lines or lines == [""]:
        return [], []
    # 결과를 반환하는 문장은 하나만 두는 것이 규칙 (SET 등 결과 없는 문장은 허용)
    header = lines[0].split("\t")
    rows = [l.split("\t") for l in lines[1:]]
    return header, rows


def to_markdown_table(header: list[str], rows: list[list[str]]) -> str:
    if not header:
        return "_(결과 없음)_"
    esc = lambda v: v.replace("|", "\\|")
    out = ["| " + " | ".join(map(esc, header)) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows[:MAX_ROWS]:
        out.append("| " + " | ".join(map(esc, r)) + " |")
    if len(rows) > MAX_ROWS:
        out.append(f"\n> 총 {len(rows)}행 중 상위 {MAX_ROWS}행만 표시")
    else:
        out.append(f"\n> 총 {len(rows)}행")
    return "\n".join(out)


def parse_problem(text: str) -> tuple[str, str]:
    """problem.md 에서 (제목, 난이도) 추출"""
    title = re.search(r"^#\s+(.+)$", text, re.M)
    level = re.search(r"^level:\s*(.+)$", text, re.M | re.I)
    return (title.group(1).strip() if title else "제목 없음",
            level.group(1).strip() if level else "-")


def build_one(pdir: Path) -> dict:
    problem = (pdir / "problem.md").read_text(encoding="utf-8")
    sql = (pdir / "solution.sql").read_text(encoding="utf-8").strip()
    analysis_path = pdir / "analysis.md"
    analysis = analysis_path.read_text(encoding="utf-8") if analysis_path.exists() else ""
    title, level = parse_problem(problem)

    header, rows = run_sql(sql)
    body_problem = re.sub(r"^level:.*\n?", "", problem, flags=re.M | re.I)
    body_problem = re.sub(r"^#\s+.+\n?", "", body_problem, count=1, flags=re.M).strip()

    readme = f"""# {pdir.name[:3]}. {title}

**난이도:** {level}

## 문제

{body_problem}

## 풀이 쿼리

```sql
{sql}
```

## 실행 결과

{to_markdown_table(header, rows)}

## 분석

{analysis.strip() or '_(분석 작성 예정)_'}
"""
    (pdir / "README.md").write_text(readme, encoding="utf-8")
    print(f"[OK] {pdir.name}: {len(rows)}행")
    return {"dir": pdir.name, "title": title, "level": level}


def write_index(items: list[dict]) -> None:
    rows = "\n".join(
        f"| {it['dir'][:3]} | [{it['title']}](problems/{it['dir']}/README.md) | {it['level']} |"
        for it in items)
    (ROOT / "README.md").write_text(f"""# Sakila MySQL 문제 풀이

MySQL 공식 샘플 DB **Sakila**(DVD 대여점)를 이용한 SQL 연습 문제 모음입니다.
각 문제 폴더에는 문제 설명, 풀이 쿼리, 실제 실행 결과, 분석이 들어 있습니다.

## 문제 목록

| 번호 | 제목 | 난이도 |
|---|---|---|
{rows}

## 실습 환경 구성

```bash
docker compose up -d          # MySQL 8 + Sakila 자동 로드 (포트 3307, root / sakila)
python scripts/build.py       # 모든 풀이 실행 → README 재생성
python scripts/build.py --push  # 빌드 후 GitHub 에 커밋/푸시
```

## 웹에서 직접 풀기

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py   # http://localhost:8501
```

- 왼쪽에서 문제를 고르고, SQL 을 작성해 **실행** / **제출(채점)** 합니다.
- 채점은 정답 쿼리 결과와 값·행 수·정렬 순서를 비교합니다.
- 맞히면 정답 쿼리와 해설이 열리고, 푼 문제는 `progress.json` 에 기록됩니다.
- 앱은 SELECT 만 가능한 읽기 전용 계정(`learner`)으로 접속하므로 데이터가 바뀌지 않습니다.

## Sakila 주요 테이블

| 테이블 | 설명 |
|---|---|
| film / film_category / category / language | 영화와 장르, 언어 |
| actor / film_actor | 배우와 출연 관계 |
| inventory | 매장별 보유 DVD 재고 |
| rental / payment | 대여 기록과 결제 |
| customer / staff / store | 고객, 직원, 매장 |
| address / city / country | 주소 계층 |
""", encoding="utf-8")


def git_push() -> None:
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        print("변경 사항 없음 — 푸시 생략")
        return
    subprocess.run(["git", "commit", "-m", "문제 풀이 결과 갱신"], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dirs = sorted(p for p in PROBLEMS.iterdir() if p.is_dir())
    items = []
    for d in dirs:
        if args and not any(d.name.startswith(a) for a in args):
            title, level = parse_problem((d / "problem.md").read_text(encoding="utf-8"))
            items.append({"dir": d.name, "title": title, "level": level})
            continue
        items.append(build_one(d))
    write_index(items)
    if "--push" in sys.argv:
        git_push()


if __name__ == "__main__":
    main()
