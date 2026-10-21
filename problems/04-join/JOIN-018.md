# JOIN-018. 영화별 재고와 대여 통계

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `조인 팬아웃` `COUNT DISTINCT`

## 문제

`film_id` 1~10번 영화별로 보유 재고 수 `copies` 와 총 대여 횟수 `rentals` 를 구하세요. 재고가 없는 영화도 0으로 포함합니다.

- `film_id` 순

**사용 테이블:** `film`, `inventory`, `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.film_id, f.title,
       COUNT(DISTINCT i.inventory_id) AS copies,
       COUNT(r.rental_id)             AS rentals
FROM film f
LEFT JOIN inventory i ON i.film_id      = f.film_id
LEFT JOIN rental r    ON r.inventory_id = i.inventory_id
WHERE f.film_id <= 10
GROUP BY f.film_id, f.title
ORDER BY f.film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title | copies | rentals |
|---|---|---|---|
| 1 | ACADEMY DINOSAUR | 8 | 23 |
| 2 | ACE GOLDFINGER | 3 | 7 |
| 3 | ADAPTATION HOLES | 4 | 12 |
| 4 | AFFAIR PREJUDICE | 7 | 23 |
| 5 | AFRICAN EGG | 3 | 12 |
| 6 | AGENT TRUMAN | 6 | 21 |
| 7 | AIRPLANE SIERRA | 5 | 15 |
| 8 | AIRPORT POLLOCK | 4 | 18 |
| 9 | ALABAMA DEVIL | 5 | 12 |
| 10 | ALADDIN CALENDAR | 7 | 23 |

> 총 10행

</details>

## 해설

1:N:M 으로 조인하면 상위 테이블 행이 **곱해집니다(팬아웃)**. 재고 1장에 대여 20건이면 재고 행이 20번 나오므로
`COUNT(i.inventory_id)` 는 틀리고 `COUNT(DISTINCT i.inventory_id)` 가 맞습니다. SUM 은 DISTINCT 로도 해결되지 않으니 집계 후 조인하세요.
