# JOIN-008. LEFT JOIN 조건 위치의 함정

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `LEFT JOIN` `ON vs WHERE`

## 문제

모든 고객(599명)에 대해 **2005년 5월** 대여 건수를 구하세요. 5월에 대여하지 않은 고객도 0으로 포함해야 합니다.

- 출력: `customer_id`, `may_rentals` — `customer_id` 순

**사용 테이블:** `customer`, `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT c.customer_id, COUNT(r.rental_id) AS may_rentals
FROM customer c
LEFT JOIN rental r
       ON r.customer_id = c.customer_id
      AND r.rental_date >= '2005-05-01'
      AND r.rental_date <  '2005-06-01'
GROUP BY c.customer_id
ORDER BY c.customer_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| customer_id | may_rentals |
|---|---|
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |
| 4 | 0 |
| 5 | 3 |
| 6 | 3 |
| 7 | 5 |
| 8 | 1 |
| 9 | 3 |
| 10 | 1 |
| 11 | 1 |
| 12 | 2 |
| 13 | 0 |
| 14 | 5 |
| 15 | 0 |
| 16 | 4 |
| 17 | 3 |
| 18 | 3 |
| 19 | 6 |
| 20 | 3 |

> 총 599행 중 상위 20행만 표시

</details>

## 해설

날짜 조건을 `WHERE` 에 두면 매칭되지 않은 고객(r.* 가 NULL)이 걸러져 **INNER JOIN 처럼** 동작합니다.
LEFT JOIN 에서 **오른쪽 테이블의 필터 조건은 ON 절에** 두어야 왼쪽 행이 보존됩니다. 결과는 599행이어야 합니다.
