# JOIN-016. 직원 간 매장 비교 (CROSS JOIN)

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `CROSS JOIN` `카테시안 곱`

## 문제

모든 매장 × 모든 등급 조합에 대해, 그 매장이 보유한 해당 등급 영화의 재고 수를 구하세요. 재고가 없는 조합도 0으로 나와야 합니다.

- 출력: `store_id`, `rating`, `copies` — `store_id`, `rating` 순

**사용 테이블:** `store`, `film`, `inventory`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT st.store_id, r.rating, COUNT(i.inventory_id) AS copies
FROM store st
CROSS JOIN (SELECT DISTINCT rating FROM film) r
LEFT JOIN film f      ON f.rating    = r.rating
LEFT JOIN inventory i ON i.film_id   = f.film_id
                     AND i.store_id = st.store_id
GROUP BY st.store_id, r.rating
ORDER BY st.store_id, r.rating;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store_id | rating | copies |
|---|---|---|
| 1 | G | 394 |
| 1 | PG | 444 |
| 1 | PG-13 | 525 |
| 1 | R | 442 |
| 1 | NC-17 | 465 |
| 2 | G | 397 |
| 2 | PG | 480 |
| 2 | PG-13 | 493 |
| 2 | R | 462 |
| 2 | NC-17 | 479 |

> 총 10행

</details>

## 해설

`CROSS JOIN` 은 조건 없이 모든 조합(카테시안 곱)을 만듭니다. 리포트의 "뼈대"를 먼저 만들고 LEFT JOIN 으로 실적을 붙이는 방식입니다.
