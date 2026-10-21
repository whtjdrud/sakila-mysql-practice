# JOIN-013. 한 번도 대여하지 않은 장르가 있는 고객

**유형:** 조인 · **난이도:** ★★★★☆ 고급 · **태그:** `CROSS JOIN` `안티 조인`

## 문제

고객 1~3번에 대해, 그 고객이 **한 번도 빌리지 않은 장르** 목록을 구하세요.

- 출력: `customer_id`, `category` — `customer_id`, `category` 순

**사용 테이블:** `customer`, `category`, `rental`, `inventory`, `film_category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT c.customer_id, cat.name AS category
FROM customer c
CROSS JOIN category cat
LEFT JOIN (
    SELECT DISTINCT r.customer_id, fc.category_id
    FROM rental r
    JOIN inventory i      ON i.inventory_id = r.inventory_id
    JOIN film_category fc ON fc.film_id     = i.film_id
) seen ON seen.customer_id = c.customer_id
      AND seen.category_id = cat.category_id
WHERE c.customer_id <= 3
  AND seen.customer_id IS NULL
ORDER BY c.customer_id, category;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| customer_id | category |
|---|---|
| 1 | Children |
| 1 | Horror |
| 2 | Comedy |
| 2 | Drama |
| 2 | Horror |
| 3 | Children |
| 3 | Foreign |
| 3 | Travel |

> 총 8행

</details>

## 해설

"없는 조합"을 찾으려면 먼저 **가능한 모든 조합**을 `CROSS JOIN` 으로 만든 뒤, 실제 데이터와 안티 조인합니다.
매출 0인 날짜/상품 채우기, 미응답자 찾기 등에 자주 쓰는 패턴입니다.
