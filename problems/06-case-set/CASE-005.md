# CASE-005. 매장 × 장르 매출 피벗

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `피벗` `SUM CASE`

## 문제

장르별로 1번 매장 매출 `store1`, 2번 매장 매출 `store2`, 차이 `diff`(store1 - store2)를 구하세요.
매장은 결제를 처리한 직원의 매장 기준입니다. `diff` 내림차순, `category` 순.

**사용 테이블:** `payment`, `staff`, `rental`, `inventory`, `film_category`, `category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT c.name AS category,
       SUM(CASE WHEN s.store_id = 1 THEN p.amount ELSE 0 END) AS store1,
       SUM(CASE WHEN s.store_id = 2 THEN p.amount ELSE 0 END) AS store2,
       SUM(CASE WHEN s.store_id = 1 THEN p.amount ELSE -p.amount END) AS diff
FROM payment p
JOIN staff s          ON s.staff_id     = p.staff_id
JOIN rental r         ON r.rental_id    = p.rental_id
JOIN inventory i      ON i.inventory_id = r.inventory_id
JOIN film_category fc ON fc.film_id     = i.film_id
JOIN category c       ON c.category_id  = fc.category_id
GROUP BY c.category_id, c.name
ORDER BY diff DESC, category;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| category | store1 | store2 | diff |
|---|---|---|---|
| Drama | 2375.44 | 2211.95 | 163.49 |
| Travel | 1844.77 | 1704.87 | 139.90 |
| Action | 2245.36 | 2130.49 | 114.87 |
| Music | 1761.77 | 1655.95 | 105.82 |
| Horror | 1910.73 | 1811.81 | 98.92 |
| Animation | 2361.08 | 2295.22 | 65.86 |
| Family | 2132.52 | 2093.55 | 38.97 |
| Sci-Fi | 2395.37 | 2361.61 | 33.76 |
| Comedy | 2195.17 | 2188.41 | 6.76 |
| Documentary | 2086.69 | 2130.83 | -44.14 |
| Sports | 2633.01 | 2681.20 | -48.19 |
| Classics | 1749.30 | 1890.29 | -140.99 |
| Foreign | 2050.95 | 2219.72 | -168.77 |
| New | 2068.52 | 2283.10 | -214.58 |
| Games | 1997.35 | 2283.98 | -286.63 |
| Children | 1674.47 | 1981.08 | -306.61 |

> 총 16행

</details>

## 해설

CASE 의 THEN 에 숫자 대신 **컬럼 값**(`p.amount`)을 넣으면 조건부 합계가 됩니다.
차이를 `store1 - store2` 로 다시 계산하는 대신 부호를 바꿔 한 번에 더하는 트릭도 있습니다.
