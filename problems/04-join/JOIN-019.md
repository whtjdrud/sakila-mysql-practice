# JOIN-019. 팬아웃으로 부풀려진 매출

**유형:** 조인 · **난이도:** ★★★★☆ 고급 · **태그:** `조인 팬아웃` `집계 후 조인`

## 문제

장르별 **실제 매출 합계**와, 출연 배우(`film_actor`)를 함께 조인했을 때 **잘못 부풀려진 합계**를 나란히 구하세요.

- 출력: `category`, `real_revenue`, `inflated_revenue`, `ratio`(inflated/real, 소수 2자리) — `category` 순

**사용 테이블:** `payment`, `rental`, `inventory`, `film_category`, `category`, `film_actor`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT r.category, r.real_revenue, x.inflated_revenue,
       ROUND(x.inflated_revenue / r.real_revenue, 2) AS ratio
FROM (
    SELECT c.name AS category, SUM(p.amount) AS real_revenue
    FROM payment p
    JOIN rental rt        ON rt.rental_id   = p.rental_id
    JOIN inventory i      ON i.inventory_id = rt.inventory_id
    JOIN film_category fc ON fc.film_id     = i.film_id
    JOIN category c       ON c.category_id  = fc.category_id
    GROUP BY c.name
) r
JOIN (
    SELECT c.name AS category, SUM(p.amount) AS inflated_revenue
    FROM payment p
    JOIN rental rt        ON rt.rental_id   = p.rental_id
    JOIN inventory i      ON i.inventory_id = rt.inventory_id
    JOIN film_category fc ON fc.film_id     = i.film_id
    JOIN category c       ON c.category_id  = fc.category_id
    JOIN film_actor fa    ON fa.film_id     = i.film_id
    GROUP BY c.name
) x ON x.category = r.category
ORDER BY r.category;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| category | real_revenue | inflated_revenue | ratio |
|---|---|---|---|
| Action | 4375.85 | 23882.67 | 5.46 |
| Animation | 4656.30 | 26945.80 | 5.79 |
| Children | 3655.55 | 20927.90 | 5.72 |
| Classics | 3639.59 | 19521.02 | 5.36 |
| Comedy | 4383.58 | 21688.33 | 4.95 |
| Documentary | 4217.52 | 23580.23 | 5.59 |
| Drama | 4587.39 | 25886.65 | 5.64 |
| Family | 4226.07 | 21111.04 | 5.00 |
| Foreign | 4270.67 | 23947.38 | 5.61 |
| Games | 4281.33 | 20008.58 | 4.67 |
| Horror | 3722.54 | 20261.71 | 5.44 |
| Music | 3417.72 | 19002.02 | 5.56 |
| New | 4351.62 | 24149.18 | 5.55 |
| Sci-Fi | 4756.98 | 24887.49 | 5.23 |
| Sports | 5314.21 | 31961.67 | 6.01 |
| Travel | 3549.64 | 19797.40 | 5.58 |

> 총 16행

</details>

## 해설

`film_actor` 를 조인하면 결제 1건이 출연 배우 수만큼 복제되어 매출이 **평균 배우 수 배**로 부풀려집니다.
"왜 매출이 전사 합계보다 크지?" 의 가장 흔한 원인입니다. 합계를 낼 때는 **집계 단위보다 세분화된 테이블을 조인하지 않도록** 주의하세요.
