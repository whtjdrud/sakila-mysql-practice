# Sakila MySQL 문제 풀이

MySQL 공식 샘플 DB **Sakila**(DVD 대여점)를 이용한 SQL 연습 문제 모음입니다.
각 문제 폴더에는 문제 설명, 풀이 쿼리, 실제 실행 결과, 분석이 들어 있습니다.

## 문제 목록

| 번호 | 제목 | 난이도 |
|---|---|---|
| 001 | [장르별 영화 수](problems/001-category-film-count/README.md) | ⭐ 하 |
| 002 | [가장 많이 대여된 영화 TOP 10](problems/002-top-rented-films/README.md) | ⭐⭐ 중 |
| 003 | [매장별 월간 매출](problems/003-monthly-store-revenue/README.md) | ⭐⭐ 중 |
| 004 | [우수 고객 순위 (윈도우 함수)](problems/004-customer-ranking/README.md) | ⭐⭐⭐ 상 |
| 005 | [카탈로그엔 있지만 재고가 없는 영화](problems/005-films-without-inventory/README.md) | ⭐⭐⭐ 상 |
| 006 | [장르별 매출 1위 배우](problems/006-top-actor-per-category/README.md) | ⭐⭐⭐⭐ 최상 |

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
