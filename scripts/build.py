"""문제 은행 빌드 스크립트

bank/*.yaml 의 모든 정답 쿼리를 실제 DB 에서 실행·검증하고
GitHub 에서 읽기 좋은 마크다운(problems/)과 루트 README 를 생성한다.

사용법:
  python scripts/build.py              # 전체 검증 + 생성
  python scripts/build.py --check      # 검증만 (파일 생성 안 함)
  python scripts/build.py SUB WIN-00   # id 접두어로 일부만 검증
  python scripts/build.py --push       # 생성 후 git commit & push
"""

import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pymysql  # noqa: E402

from sakila_bank import (CATEGORIES, CATEGORY_BY_CODE, LEVELS, ROOT,  # noqa: E402
                         level_label, load_bank, run_query)

PROBLEMS = ROOT / "problems"
MAX_ROWS = 20  # 마크다운에 표시할 최대 행 수


def to_markdown_table(df) -> str:
    if df.empty and not len(df.columns):
        return "_(결과 없음)_"
    esc = lambda v: "NULL" if v is None else str(v).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(map(esc, df.columns)) + " |",
           "|" + "|".join("---" for _ in df.columns) + "|"]
    for row in df.head(MAX_ROWS).itertuples(index=False):
        out.append("| " + " | ".join(map(esc, row)) + " |")
    suffix = f"총 {len(df)}행 중 상위 {MAX_ROWS}행만 표시" if len(df) > MAX_ROWS else f"총 {len(df)}행"
    return "\n".join(out) + f"\n\n> {suffix}"


def validate_meta(problems: list[dict]) -> list[str]:
    errors = []
    dup = [k for k, v in Counter(p["id"] for p in problems).items() if v > 1]
    errors += [f"중복 id: {d}" for d in dup]
    for p in problems:
        if not p["id"].startswith(p["category"] + "-"):
            errors.append(f"{p['id']}: 파일 유형({p['category']})과 id 접두어 불일치")
        if p.get("level") not in LEVELS:
            errors.append(f"{p['id']}: level 은 1~5")
    return errors


def problem_markdown(p: dict, df) -> str:
    tags = " ".join(f"`{t}`" for t in p["tags"])
    return f"""# {p['id']}. {p['title']}

**유형:** {p['category_name']} · **난이도:** {level_label(p['level'])} · **태그:** {tags}

## 문제

{p['question']}

<details>
<summary>정답 쿼리 보기</summary>

```sql
{p['solution']}
```

</details>

<details>
<summary>실행 결과 보기</summary>

{to_markdown_table(df)}

</details>

## 해설

{p['note'] or '_(해설 없음)_'}
"""


def write_outputs(problems: list[dict]) -> None:
    if PROBLEMS.exists():
        shutil.rmtree(PROBLEMS)
    for code, folder, name, desc in CATEGORIES:
        items = [p for p in problems if p["category"] == code]
        if not items:
            continue
        d = PROBLEMS / folder
        d.mkdir(parents=True)
        for p in items:
            (d / f"{p['id']}.md").write_text(p["_md"], encoding="utf-8")
        rows = "\n".join(
            f"| [{p['id']}]({p['id']}.md) | {p['title']} | {level_label(p['level'])} | {', '.join(p['tags'])} |"
            for p in items)
        (d / "README.md").write_text(
            f"# {name}\n\n{desc}\n\n| ID | 제목 | 난이도 | 태그 |\n|---|---|---|---|\n{rows}\n",
            encoding="utf-8")
    write_root_readme(problems)


def write_root_readme(problems: list[dict]) -> None:
    lv = sorted(LEVELS)
    head = "| 유형 | 내용 | " + " | ".join(LEVELS[l] for l in lv) + " | 합계 |"
    sep = "|---|---|" + "---|" * (len(lv) + 1)
    lines = [head, sep]
    for code, folder, name, desc in CATEGORIES:
        items = [p for p in problems if p["category"] == code]
        if not items:
            continue
        c = Counter(p["level"] for p in items)
        lines.append(f"| [{name}](problems/{folder}/README.md) | {desc} | "
                     + " | ".join(str(c.get(l, 0) or "-") for l in lv) + f" | **{len(items)}** |")
    total = Counter(p["level"] for p in problems)
    lines.append("| **합계** | | " + " | ".join(f"**{total.get(l, 0)}**" for l in lv)
                 + f" | **{len(problems)}** |")
    matrix = "\n".join(lines)

    (ROOT / "README.md").write_text(f"""# Sakila MySQL 문제 풀이

MySQL 공식 샘플 DB **Sakila**(DVD 대여점)로 만든 SQL 연습 문제 **{len(problems)}개**입니다.
모든 정답 쿼리는 실제 DB 에서 실행·검증되었고, 문제마다 실행 결과와 해설이 들어 있습니다.

## 문제 현황 (유형 × 난이도)

{matrix}

난이도: ★ 입문 → ★★★★★ 최고급

## 웹에서 직접 풀기

```bash
docker compose up -d             # MySQL 8 + Sakila 자동 로드 (포트 3307)
pip install -r requirements.txt
streamlit run streamlit_app.py   # http://localhost:8501
```

- **문제 목록**에서 유형·난이도·태그·풀이 상태로 필터링하고, 행을 클릭하면 바로 풀이 화면으로 이동합니다.
- **문제 풀기**에서 SQL 을 작성해 **실행** / **제출(채점)** 합니다. 채점은 정답 쿼리 결과와 값·행 수·정렬 순서를 비교합니다.
- 맞히면 정답 쿼리와 해설이 열리고, 푼 문제는 `progress.json` 에 기록됩니다.
- 앱은 SELECT 만 가능한 읽기 전용 계정(`learner`)으로 접속하므로 데이터가 바뀌지 않습니다.

## 문제 추가하기

`bank/<유형코드>.yaml` 에 문제를 추가하고 `python scripts/build.py` 로 검증합니다.
형식은 [sakila_bank.py](sakila_bank.py) 상단 주석을 참고하세요.

## Sakila 주요 테이블

| 테이블 | 설명 |
|---|---|
| film / film_category / category / language | 영화와 장르, 언어 |
| actor / film_actor | 배우와 출연 관계 |
| inventory | 매장별 보유 DVD 재고 (영화 1편 = 여러 장) |
| rental / payment | 대여 기록과 결제 |
| customer / staff / store | 고객, 직원, 매장 |
| address / city / country | 주소 계층 |
""", encoding="utf-8")


def git_push() -> None:
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        print("변경 사항 없음 — 푸시 생략")
        return
    subprocess.run(["git", "commit", "-m", "문제 은행 갱신"], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def main() -> None:
    prefixes = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv or bool(prefixes)
    problems = load_bank()
    meta_errors = validate_meta(problems)
    for e in meta_errors:
        print(f"[META] {e}")

    failed, empty, slow = [], [], []
    for p in problems:
        if prefixes and not any(p["id"].startswith(x) for x in prefixes):
            continue
        t = time.perf_counter()
        try:
            df = run_query(p["solution"])
        except pymysql.MySQLError as e:
            failed.append(p["id"])
            print(f"[FAIL] {p['id']}: {e}")
            continue
        sec = time.perf_counter() - t
        if len(df) == 0:
            empty.append(p["id"])
        if sec > 3:
            slow.append(p["id"])
        p["_md"] = problem_markdown(p, df)
        if prefixes:
            print(f"[OK] {p['id']} ({len(df)}행, {sec:.2f}s)")

    by_cat = Counter(p["category"] for p in problems)
    print(f"\n총 {len(problems)}문제 · " + ", ".join(f"{c} {by_cat[c]}" for c, *_ in CATEGORIES if by_cat[c]))
    print(f"실패 {len(failed)} · 0행 {len(empty)} {empty} · 3초 초과 {slow}")

    if meta_errors or failed:
        sys.exit(1)
    if not check_only:
        write_outputs(problems)
        print("problems/ 와 README.md 생성 완료")
        if "--push" in sys.argv:
            git_push()


if __name__ == "__main__":
    main()
