# CASE-015. 매장별 신규 vs 재방문 비율

**유형:** 조건식·집합 · **난이도:** ★★★★☆ 고급 · **태그:** `CASE` `상관 서브쿼리` `비율`

## 문제

2005년 7월 대여를 **그 고객의 첫 대여인지 여부**로 나눠, 매장(`inventory.store_id`)별 신규 대여 건수와 재방문 대여 건수, 신규 비율을 구하세요.

- 출력: `store_id`, `first_time`, `returning`, `first_pct`(소수 2자리) — `store_id` 순

**사용 테이블:** `rental`, `inventory`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT i.store_id,
       SUM(CASE WHEN r.rental_date = fr.first_date THEN 1 ELSE 0 END) AS first_time,
       SUM(CASE WHEN r.rental_date > fr.first_date THEN 1 ELSE 0 END) AS returning,
       ROUND(100 * AVG(r.rental_date = fr.first_date), 2) AS first_pct
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN (
    SELECT customer_id, MIN(rental_date) AS first_date
    FROM rental
    GROUP BY customer_id
) fr ON fr.customer_id = r.customer_id
WHERE r.rental_date >= '2005-07-01' AND r.rental_date < '2005-08-01'
GROUP BY i.store_id
ORDER BY i.store_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store_id | first_time | returning | first_pct |
|---|---|---|---|
| 1 | 1 | 3333 | 0.03 |
| 2 | 0 | 3375 | 0.00 |

> 총 2행

</details>

## 해설

599명 중 598명의 첫 대여가 2005년 5~6월이라, 7월 신규 대여는 **단 1건**(1번 매장)입니다.
이처럼 0에 가까운 지표는 "왜 그런지" 를 데이터 기간과 함께 설명할 수 있어야 합니다. 기간을 5월로 바꿔 비교해 보세요.
