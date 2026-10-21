# JOIN-004. 대여 상세 내역

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `다중 조인`

## 문제

고객 `MARY SMITH` 의 대여 내역을 최근 순으로 5건 조회하세요.

- 출력: `rental_date`, `title`, `store_id`(재고가 있는 매장), `return_date`
- `rental_date` 내림차순

**사용 테이블:** `customer`, `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT r.rental_date, f.title, i.store_id, r.return_date
FROM customer c
JOIN rental r    ON r.customer_id  = c.customer_id
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
WHERE c.first_name = 'MARY' AND c.last_name = 'SMITH'
ORDER BY r.rental_date DESC
LIMIT 5;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rental_date | title | store_id | return_date |
|---|---|---|---|
| 2005-08-22 20:03:46 | BIKINI BORROWERS | 1 | 2005-08-30 01:51:46 |
| 2005-08-22 19:41:37 | FIREBALL PHILADELPHIA | 1 | 2005-08-28 22:49:37 |
| 2005-08-22 01:27:57 | FIREBALL PHILADELPHIA | 2 | 2005-08-27 07:01:57 |
| 2005-08-21 23:33:57 | UNFORGIVEN ZOOLANDER | 1 | 2005-08-23 01:30:57 |
| 2005-08-19 13:56:54 | JUMANJI BLADE | 1 | 2005-08-23 08:50:54 |

> 총 5행

</details>

## 해설

대여는 영화가 아니라 **재고(DVD 1장)** 를 가리킵니다. `rental → inventory → film` 경로는 Sakila 에서 가장 많이 쓰는 조인입니다.
