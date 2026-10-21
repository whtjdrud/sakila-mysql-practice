# 005. 카탈로그엔 있지만 재고가 없는 영화

**난이도:** ⭐⭐⭐ 상

## 문제

`film` 테이블에는 등록되어 있지만 **어느 매장에도 재고(inventory)가 없는** 영화를 찾으세요.
장르도 함께 출력합니다.

- 출력 컬럼: `film_id`, `title`, `category`
- `film_id` 오름차순

**생각해볼 점:** `LEFT JOIN ... IS NULL` 과 `NOT EXISTS` 중 무엇을 쓸까요?
그리고 "재고는 있지만 한 번도 대여되지 않은 영화"는 몇 편일까요?

**사용 테이블:** `film`, `inventory`, `film_category`, `category`

## 풀이 쿼리

```sql
SELECT f.film_id,
       f.title,
       c.name AS category
FROM film f
LEFT JOIN inventory i     ON i.film_id      = f.film_id
JOIN film_category fc     ON fc.film_id     = f.film_id
JOIN category c           ON c.category_id  = fc.category_id
WHERE i.inventory_id IS NULL
ORDER BY f.film_id;
```

## 실행 결과

| film_id | title | category |
|---|---|---|
| 14 | ALICE FANTASIA | Classics |
| 33 | APOLLO TEEN | Drama |
| 36 | ARGONAUTS TOWN | Animation |
| 38 | ARK RIDGEMONT | Action |
| 41 | ARSENIC INDEPENDENCE | Travel |
| 87 | BOONDOCK BALLROOM | Travel |
| 108 | BUTCH PANTHER | New |
| 128 | CATCH AMISTAD | Foreign |
| 144 | CHINATOWN GLADIATOR | New |
| 148 | CHOCOLATE DUCK | Foreign |
| 171 | COMMANDMENTS EXPRESS | Horror |
| 192 | CROSSING DIVORCE | Foreign |
| 195 | CROWDS TELEMARK | Sci-Fi |
| 198 | CRYSTAL BREAKING | Foreign |
| 217 | DAZED PUNK | Games |
| 221 | DELIVERANCE MULHOLLAND | Documentary |
| 318 | FIREHOUSE VIETNAM | Action |
| 325 | FLOATS GARDEN | Animation |
| 332 | FRANKENSTEIN STRANGER | Comedy |
| 359 | GLADIATOR WESTWARD | Family |

> 총 42행 중 상위 20행만 표시

## 분석

### 핵심 개념
- **안티 조인(Anti Join)**: "B 에 없는 A" 를 찾는 패턴입니다.
  - `LEFT JOIN B ... WHERE B.pk IS NULL`
  - `WHERE NOT EXISTS (SELECT 1 FROM B WHERE ...)`
- 둘 다 MySQL 8 옵티마이저가 같은 안티 조인으로 변환하는 경우가 많습니다. 다만 `NOT IN (subquery)` 는 서브쿼리에 NULL 이 하나라도 있으면 **결과가 0행**이 되는 함정이 있으니 피하는 것이 좋습니다.
- `IS NULL` 검사는 반드시 **NOT NULL 컬럼(보통 PK)** 에 해야 합니다. 원래 NULL 일 수 있는 컬럼을 검사하면 "매칭 실패"와 "값이 NULL"을 구분할 수 없습니다.

### 결과 해석
- 1,000편 중 **42편(4.2%)** 은 어느 매장에도 재고가 없습니다.
- 장르별로는 Foreign(6편), Documentary(5편), Travel(4편) 순으로 많습니다.
- 매장 1은 759편/2,270장, 매장 2는 762편/2,311장을 보유하고 있습니다.

### 💡 "재고는 있는데 한 번도 대여되지 않은 영화"는?
**0편**입니다. 재고가 있는 958편은 모두 최소 1회 이상 대여되었습니다.
단, **DVD 실물 단위**로 보면 미대여 재고가 딱 1장 있습니다 — `inventory_id = 5` (매장 2의 ACADEMY DINOSAUR).
"영화 단위"냐 "재고 단위"냐에 따라 답이 완전히 달라지므로, 집계 단위를 먼저 정의하는 습관이 중요합니다.
