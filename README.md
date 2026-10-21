# Sakila MySQL 문제 풀이

MySQL 공식 샘플 DB **Sakila**(DVD 대여점)로 만든 SQL 연습 문제 **212개**입니다.
모든 정답 쿼리는 실제 DB 에서 실행·검증되었고, 문제마다 실행 결과와 해설이 들어 있습니다.

## 문제 현황 (유형 × 난이도)

| 유형 | 내용 | 입문 | 초급 | 중급 | 고급 | 최고급 | 합계 |
|---|---|---|---|---|---|---|---|
| [기본 조회](problems/01-basic-select/README.md) | SELECT · WHERE · ORDER BY · LIMIT · DISTINCT | 11 | 9 | 2 | - | - | **22** |
| [함수](problems/02-functions/README.md) | 문자열 · 숫자 · 날짜 함수, NULL 처리 | 7 | 11 | 5 | - | - | **23** |
| [집계](problems/03-aggregate/README.md) | 집계 함수 · GROUP BY · HAVING · ROLLUP | 5 | 14 | 7 | - | - | **26** |
| [조인](problems/04-join/README.md) | INNER · LEFT · SELF · 다중 조인 · 안티 조인 | 4 | 8 | 7 | 5 | - | **24** |
| [서브쿼리](problems/05-subquery/README.md) | 스칼라 · IN · EXISTS · 상관 · 파생 테이블 | 4 | 8 | 13 | 7 | 3 | **35** |
| [조건식·집합](problems/06-case-set/README.md) | CASE · 피벗 · UNION · 집합 연산 | 2 | 6 | 7 | 2 | 1 | **18** |
| [CTE](problems/07-cte/README.md) | WITH · 다단계 CTE · 재귀 CTE | - | 4 | 5 | 7 | 2 | **18** |
| [윈도우 함수](problems/08-window/README.md) | 순위 · 누적 · 이동 평균 · LAG/LEAD | - | 8 | 12 | 6 | - | **26** |
| [복합 분석](problems/09-advanced/README.md) | 코호트 · 리텐션 · 갭/섬 · 실무형 리포트 | - | - | - | 10 | 10 | **20** |
| **합계** | | **33** | **68** | **58** | **37** | **16** | **212** |

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
