# 006. 장르별 매출 1위 배우

**난이도:** ⭐⭐⭐⭐ 최상

## 문제

각 장르에서, 출연 영화들이 벌어들인 **매출 합계가 가장 큰 배우**를 구하세요.

- 출력 컬럼: `category`, `actor`(이름 성), `revenue`
- 동점이면 모두 출력 (`RANK()` 사용)
- 장르명 오름차순

**힌트:** 결제 → 대여 → 재고 → 영화 → (장르, 배우) 로 이어지는 6단 조인입니다.
영화 한 편의 매출은 출연 배우 모두에게 각각 집계됩니다.

**사용 테이블:** `payment`, `rental`, `inventory`, `film_category`, `category`, `film_actor`, `actor`

## 풀이 쿼리

```sql
WITH actor_revenue AS (
    SELECT cat.name AS category,
           a.actor_id,
           CONCAT(a.first_name, ' ', a.last_name) AS actor,
           SUM(p.amount) AS revenue
    FROM payment p
    JOIN rental r         ON r.rental_id     = p.rental_id
    JOIN inventory i      ON i.inventory_id  = r.inventory_id
    JOIN film_category fc ON fc.film_id      = i.film_id
    JOIN category cat     ON cat.category_id = fc.category_id
    JOIN film_actor fa    ON fa.film_id      = i.film_id
    JOIN actor a          ON a.actor_id      = fa.actor_id
    GROUP BY cat.name, a.actor_id, actor
), ranked AS (
    SELECT *, RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
    FROM actor_revenue
)
SELECT category, actor, revenue
FROM ranked
WHERE rnk = 1
ORDER BY category, actor;
```

## 실행 결과

| category | actor | revenue |
|---|---|---|
| Action | RIP CRAWFORD | 466.22 |
| Animation | JAYNE NOLTE | 621.67 |
| Children | CHRISTIAN AKROYD | 410.35 |
| Classics | RAY JOHANSSON | 362.22 |
| Comedy | DARYL CRAWFORD | 452.13 |
| Documentary | JULIA BARRYMORE | 582.12 |
| Drama | CAMERON ZELLWEGER | 602.02 |
| Family | RIP CRAWFORD | 397.07 |
| Foreign | HUMPHREY WILLIS | 455.08 |
| Games | RIP WINSLET | 435.02 |
| Horror | TOM MIRANDA | 509.90 |
| Music | GINA DEGENERES | 415.24 |
| New | GRACE MOSTEL | 424.24 |
| Sci-Fi | GINA DEGENERES | 581.84 |
| Sports | BEN WILLIS | 900.43 |
| Travel | GEOFFREY HESTON | 458.19 |

> 총 16행

## 분석

### 핵심 개념
- 6단 조인 → 집계 → `RANK() OVER (PARTITION BY category ...)` → `rnk = 1` 필터링. **"그룹별 1등"** 을 구하는 정석 패턴입니다.
- MySQL 5.7 이하처럼 윈도우 함수가 없다면 "그룹별 MAX 를 구한 뒤 다시 조인"하는 방식을 써야 해서 훨씬 복잡해집니다.

### ⚠️ 매출 중복 집계 주의
영화 한 편에는 여러 배우가 출연하므로, `film_actor` 를 조인하는 순간 **결제 1건이 배우 수만큼 복제**됩니다.
- 이 문제처럼 "배우별 기여 매출"을 보는 것이 목적이면 맞는 결과입니다.
- 하지만 이 결과의 `revenue` 를 모두 더해 "장르 총매출"이라고 하면 **실제보다 몇 배 부풀려진 값**이 됩니다.

또한 `payment.rental_id` 가 NULL 인 결제가 **5건(9.95)** 있어, INNER JOIN 에서 자연스럽게 제외되었습니다.

### 결과 해석
- **Sports 의 BEN WILLIS(900.43)** 가 압도적입니다. 2위권(Animation 621.67, Drama 602.02)보다 약 300 높은데, Sports 장르 영화에만 **9편** 출연했기 때문입니다. 즉 "흥행작"보다는 **출연 편수**가 큰 영향을 줍니다.
- **RIP CRAWFORD** 는 Action 과 Family 두 장르에서 1위, **GINA DEGENERES** 는 Music 과 Sci-Fi 두 장르에서 1위입니다.
- 16개 장르 모두 동점 없이 1명씩 나왔습니다.

### 더 해보기
- 출연 편수 영향을 없애려면 `SUM(p.amount) / COUNT(DISTINCT i.film_id)` 로 **편당 평균 매출**을 비교해 보세요.
