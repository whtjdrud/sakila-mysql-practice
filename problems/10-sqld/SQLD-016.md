# SQLD-016. CUBE 흉내내기

**유형:** SQLD 유형 · **난이도:** ★★★★☆ 고급 · **태그:** `CUBE` `ROLLUP` `UNION ALL` `GROUPING`

## 문제

MySQL 에는 `CUBE` 가 없습니다. 매장(`staff.store_id`) × 등급(`film.rating`) 매출을 **CUBE** 처럼 집계하세요.
즉 (매장, 등급), (매장 소계), (등급 소계), (총계) 네 종류의 행이 모두 있어야 합니다.

- 출력: `store`, `rating`, `revenue` — 소계·총계는 해당 칸을 `'ALL'` 로 표시
- 정렬: `store`, `rating` 순 (`'ALL'` 은 각각 마지막). 등급은 G → PG → PG-13 → R → NC-17 순서

**사용 테이블:** `payment`, `staff`, `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
WITH base AS (
    SELECT CAST(s.store_id AS CHAR) AS store, CAST(f.rating AS CHAR) AS rating, p.amount
    FROM payment p
    JOIN staff s     ON s.staff_id     = p.staff_id
    JOIN rental r    ON r.rental_id    = p.rental_id
    JOIN inventory i ON i.inventory_id = r.inventory_id
    JOIN film f      ON f.film_id      = i.film_id
), cubed AS (
    SELECT IF(GROUPING(store) = 1, 'ALL', store) AS store,
           IF(GROUPING(rating) = 1, 'ALL', rating) AS rating,
           SUM(amount) AS revenue
    FROM base GROUP BY store, rating WITH ROLLUP
    UNION ALL
    SELECT 'ALL', rating, SUM(amount) FROM base GROUP BY rating
)
SELECT store, rating, revenue
FROM cubed
ORDER BY store = 'ALL', store, FIELD(rating, 'G', 'PG', 'PG-13', 'R', 'NC-17', 'ALL');
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store | rating | revenue |
|---|---|---|
| 1 | G | 5758.36 |
| 1 | PG | 6636.88 |
| 1 | PG-13 | 7322.44 |
| 1 | R | 6746.53 |
| 1 | NC-17 | 7018.29 |
| 1 | ALL | 33482.50 |
| 2 | G | 5905.87 |
| 2 | PG | 6701.03 |
| 2 | PG-13 | 7936.72 |
| 2 | R | 6523.66 |
| 2 | NC-17 | 6856.78 |
| 2 | ALL | 33924.06 |
| ALL | G | 11664.23 |
| ALL | PG | 13337.91 |
| ALL | PG-13 | 15259.16 |
| ALL | R | 13270.19 |
| ALL | NC-17 | 13875.07 |
| ALL | ALL | 67406.56 |

> 총 18행

</details>

## 해설

`ROLLUP(a, b)` 는 (a,b), (a), () 만 만듭니다. `CUBE(a, b)` 는 여기에 **(b) 소계**까지 모든 조합을 만듭니다.
그래서 ROLLUP 결과에 "등급별 소계"를 `UNION ALL` 로 추가하면 CUBE 와 같아집니다. 그룹 수: ROLLUP 은 n+1 종류, CUBE 는 2ⁿ 종류.
참고: MySQL 8.0 에서 `CUBE` 는 **예약어**라 CTE 이름으로 쓸 수 없습니다 (그래서 `cubed`).
