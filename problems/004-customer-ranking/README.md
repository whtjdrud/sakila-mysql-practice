# 004. 우수 고객 순위 (윈도우 함수)

**난이도:** ⭐⭐⭐ 상

## 문제

고객별 총 결제 금액을 구하고, 전체 순위와 **국가 내 순위**를 함께 출력하세요.
전체 순위 상위 10명만 출력합니다.

- 출력 컬럼: `customer`(이름 성), `country`, `total_paid`, `overall_rank`, `country_rank`
- 순위는 동점 시 같은 순위를 주는 `RANK()` 사용

**사용 테이블:** `payment`, `customer`, `address`, `city`, `country`

## 풀이 쿼리

```sql
WITH totals AS (
    SELECT c.customer_id,
           CONCAT(c.first_name, ' ', c.last_name) AS customer,
           co.country,
           SUM(p.amount) AS total_paid
    FROM payment p
    JOIN customer c ON c.customer_id = p.customer_id
    JOIN address a  ON a.address_id  = c.address_id
    JOIN city ci    ON ci.city_id    = a.city_id
    JOIN country co ON co.country_id = ci.country_id
    GROUP BY c.customer_id, customer, co.country
), ranked AS (
    SELECT customer, country, total_paid,
           RANK() OVER (ORDER BY total_paid DESC)                      AS overall_rank,
           RANK() OVER (PARTITION BY country ORDER BY total_paid DESC) AS country_rank
    FROM totals
)
SELECT *
FROM ranked
WHERE overall_rank <= 10
ORDER BY overall_rank, customer;
```

## 실행 결과

| customer | country | total_paid | overall_rank | country_rank |
|---|---|---|---|---|
| KARL SEAL | United States | 221.55 | 1 | 1 |
| ELEANOR HUNT | Runion | 216.54 | 2 | 1 |
| CLARA SHAW | Belarus | 195.58 | 3 | 1 |
| MARION SNYDER | Brazil | 194.61 | 4 | 1 |
| RHONDA KENNEDY | Netherlands | 194.61 | 4 | 1 |
| TOMMY COLLAZO | Iran | 186.62 | 6 | 1 |
| WESLEY BULL | Spain | 177.60 | 7 | 1 |
| TIM CARY | India | 175.61 | 8 | 1 |
| MARCIA DEAN | Philippines | 175.58 | 9 | 1 |
| ANA BRADLEY | United States | 174.66 | 10 | 2 |

> 총 10행

## 분석

### 핵심 개념
- **CTE(`WITH`)** 로 단계를 나눴습니다: ① 고객별 합계 → ② 순위 계산 → ③ 필터링.
- 윈도우 함수 결과는 같은 SELECT 의 `WHERE` 에서 쓸 수 없습니다. 그래서 `ranked` CTE 로 한 번 감싼 뒤 `WHERE overall_rank <= 10` 을 적용했습니다.
- `PARTITION BY country` 는 국가별로 순위를 **다시 1부터** 매깁니다. GROUP BY 와 달리 행이 줄어들지 않는다는 점이 핵심입니다.

### 결과 해석
- 1위는 **KARL SEAL(미국, 221.55)** — 결제 45건입니다.
- **MARION SNYDER 와 RHONDA KENNEDY 가 194.61 로 공동 4위**이고, 다음 순위는 5가 아니라 **6**입니다. 이것이 `RANK()` 의 특징입니다. (`DENSE_RANK()` 면 5, `ROW_NUMBER()` 면 동점이어도 4·5로 갈립니다.)
- 상위 10명 중 9명이 각 국가 내 1위인데, **ANA BRADLEY 만 국가 내 2위**입니다. 같은 미국의 KARL SEAL 이 있기 때문이죠.
- `Runion` 은 오타가 아니라 Sakila 원본 데이터의 표기(Réunion 의 악센트 문자가 빠진 것)입니다.
