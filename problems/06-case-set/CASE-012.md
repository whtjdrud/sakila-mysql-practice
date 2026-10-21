# CASE-012. 가격 인상 시뮬레이션

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `CASE` `시뮬레이션`

## 문제

다음 규칙으로 대여료를 조정했을 때, 2005년 7월 결제가 조정 대여료로 이뤄졌다고 가정한 예상 매출을 구하세요.

- 대여 횟수 상위 인기작(영화별 대여 30회 이상): +1.00
- 등급 `NC-17`: +0.50 (인기작이면 인기작 규칙만 적용)
- 그 외: 변동 없음

출력: `actual`(실제 7월 대여료 합계 = 7월 대여 건수 × 원래 대여료), `simulated`(조정 후 합계), `uplift_pct`(소수 1자리)

**사용 테이블:** `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT SUM(f.rental_rate) AS actual,
       SUM(f.rental_rate + CASE WHEN pop.rentals >= 30 THEN 1.00
                                WHEN f.rating = 'NC-17' THEN 0.50
                                ELSE 0 END) AS simulated,
       ROUND(100 * (SUM(f.rental_rate + CASE WHEN pop.rentals >= 30 THEN 1.00
                                             WHEN f.rating = 'NC-17' THEN 0.50
                                             ELSE 0 END) / SUM(f.rental_rate) - 1), 1) AS uplift_pct
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
JOIN (
    SELECT i.film_id, COUNT(*) AS rentals
    FROM rental r JOIN inventory i ON i.inventory_id = r.inventory_id
    GROUP BY i.film_id
) pop ON pop.film_id = f.film_id
WHERE r.rental_date >= '2005-07-01' AND r.rental_date < '2005-08-01';
```

</details>

<details>
<summary>실행 결과 보기</summary>

| actual | simulated | uplift_pct |
|---|---|---|
| 19775.91 | 20804.91 | 5.2 |

> 총 1행

</details>

## 해설

가격 정책 같은 **"만약 ~라면"** 시나리오를 CASE 로 빠르게 시뮬레이션할 수 있습니다.
실제 결제(`payment.amount`)에는 연체료가 섞여 있어 대여료 효과만 보려면 `rental_rate` 기준으로 계산해야 합니다.
