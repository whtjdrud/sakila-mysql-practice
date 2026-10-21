# CASE-011. NULL 을 포함한 CASE

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `CASE` `IS NULL`

## 문제

대여를 반납 상태로 분류해 상태별 건수를 구하세요.

| 상태 | 조건 |
|---|---|
| 미반납 | return_date 가 NULL |
| 당일반납 | 대여일과 반납일이 같은 날 |
| 기한내 | 대여 기간(`rental_duration`) 이내 |
| 연체 | 그 외 |

- 출력: `status`, `rentals` — 미반납 → 당일반납 → 기한내 → 연체 순

**사용 테이블:** `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT status, COUNT(*) AS rentals
FROM (
    SELECT CASE WHEN r.return_date IS NULL THEN '미반납'
                WHEN DATE(r.return_date) = DATE(r.rental_date) THEN '당일반납'
                WHEN DATEDIFF(r.return_date, r.rental_date) <= f.rental_duration THEN '기한내'
                ELSE '연체' END AS status
    FROM rental r
    JOIN inventory i ON i.inventory_id = r.inventory_id
    JOIN film f      ON f.film_id      = i.film_id
) t
GROUP BY status
ORDER BY FIELD(status, '미반납', '당일반납', '기한내', '연체');
```

</details>

<details>
<summary>실행 결과 보기</summary>

| status | rentals |
|---|---|
| 미반납 | 183 |
| 당일반납 | 105 |
| 기한내 | 8487 |
| 연체 | 7269 |

> 총 4행

</details>

## 해설

NULL 검사는 **가장 먼저** 해야 합니다. `DATEDIFF(NULL, ...)` 은 NULL 이고 `NULL <= 3` 도 NULL(거짓 취급)이라
NULL 검사를 빼먹으면 미반납이 `연체` 로 잘못 분류됩니다.
