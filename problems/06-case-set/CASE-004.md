# CASE-004. 등급별 월간 대여 피벗

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `피벗` `조건부 집계`

## 문제

영화 등급을 행으로, 대여 월(2005-05 ~ 2005-08)을 열로 하는 대여 건수 피벗 표를 만드세요.

- 출력: `rating`, `m05`, `m06`, `m07`, `m08`, `total` — `rating` 순

**사용 테이블:** `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.rating,
       SUM(MONTH(r.rental_date) = 5 AND YEAR(r.rental_date) = 2005) AS m05,
       SUM(MONTH(r.rental_date) = 6 AND YEAR(r.rental_date) = 2005) AS m06,
       SUM(MONTH(r.rental_date) = 7 AND YEAR(r.rental_date) = 2005) AS m07,
       SUM(MONTH(r.rental_date) = 8 AND YEAR(r.rental_date) = 2005) AS m08,
       COUNT(*) AS total
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
GROUP BY f.rating
ORDER BY f.rating;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating | m05 | m06 | m07 | m08 | total |
|---|---|---|---|---|---|
| G | 212 | 393 | 1189 | 946 | 2773 |
| PG | 216 | 459 | 1348 | 1155 | 3212 |
| PG-13 | 265 | 517 | 1515 | 1246 | 3585 |
| R | 227 | 479 | 1315 | 1131 | 3181 |
| NC-17 | 236 | 463 | 1342 | 1208 | 3293 |

> 총 5행

</details>

## 해설

MySQL 에는 `PIVOT` 문법이 없어 **조건부 집계**로 피벗합니다. 열 하나 = `SUM(CASE WHEN 조건 THEN 1 ELSE 0 END)`.
`total` 은 2006-02 대여까지 포함하므로 m05~m08 합계와 다릅니다 — 의도한 것인지 항상 확인하세요.
