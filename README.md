# Sakila MySQL 문제 풀이

MySQL 공식 샘플 DB **Sakila**(DVD 대여점)로 만든 SQL 연습 문제 **274개**입니다.
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
| [SQLD 유형](problems/10-sqld/README.md) | SQLD 빈출 개념 · Oracle 문법과의 차이 · EMP 계층 질의 | 4 | 13 | 7 | 2 | - | **26** |
| [실무 요청](problems/11-business/README.md) | 현업 요청서 형식 · 지표 정의 · 추출 · 리포트 | - | - | 11 | 8 | 1 | **20** |
| [쿼리 디버깅](problems/12-debug/README.md) | 잘못된 쿼리 고치기 · 팬아웃 · NULL · 조인 조건 | - | 8 | 8 | - | - | **16** |
| **합계** | | **37** | **89** | **84** | **47** | **17** | **274** |

난이도: ★ 입문 → ★★★★★ 최고급

## 웹에서 직접 풀기

```bash
docker compose up -d             # MySQL 8 + Sakila 자동 로드 (포트 3307)
pip install -r requirements.txt
streamlit run streamlit_app.py   # http://localhost:8501
```

| 페이지 | 기능 |
|---|---|
| 문제 목록 | 유형·난이도·풀이 상태·검색 필터, 행 클릭 시 풀이 화면으로 이동 |
| 문제 풀기 | Workbench 스타일 SQL 에디터, 채점, 정답·해설 |
| 스키마 탐색 | 테이블·뷰 목록, 컬럼, FK 관계, 샘플 데이터, DDL |
| 학습 통계 | 해결률, 첫 제출 정답률, 유형 × 난이도 해결률, 일별 활동, 막힌 문제, 추천 문제 |

**에디터 단축키**

| 키 | 동작 |
|---|---|
| `Ctrl+Enter` | 선택 영역 실행 (선택이 없으면 커서가 있는 문장) |
| `Ctrl+Shift+Enter` | 선택 영역 실행 (선택이 없으면 전체) — 결과는 문장별 탭으로 |
| `Ctrl+S` | 제출(채점) — 대상은 `Ctrl+Enter` 와 같음 |

- 채점은 정답 쿼리 결과와 값·행 수·정렬 순서를 비교합니다. 제출 기록은 `progress.json` 에 저장됩니다.
- **실무 모드**(사이드바)를 켜면 문제의 "사용 테이블" 힌트와 테이블 구조 탭이 숨겨집니다. `SHOW TABLES;`, `DESCRIBE 테이블;` 이나 스키마 탐색 페이지로 직접 찾아보세요.
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
