# SQLD-011. FULL OUTER JOIN 흉내내기

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `FULL OUTER JOIN` `UNION`

## 문제

MySQL 에는 FULL OUTER JOIN 이 없습니다. 아래 두 집합을 **FULL OUTER JOIN** 한 결과를 만드세요.

- A: 1번 매장(`customer.store_id = 1`) 고객이 사는 국가별 고객 수
- B: 2번 매장 고객이 사는 국가별 고객 수

출력: `country`, `store1`, `store2` (없는 쪽은 NULL) — `country` 순

**사용 테이블:** `customer`, `address`, `city`, `country`

<details>
<summary>정답 쿼리 보기</summary>

```sql
WITH cc AS (
    SELECT co.country, c.store_id, COUNT(*) AS n
    FROM customer c
    JOIN address a  ON a.address_id  = c.address_id
    JOIN city ci    ON ci.city_id    = a.city_id
    JOIN country co ON co.country_id = ci.country_id
    GROUP BY co.country, c.store_id
), a AS (SELECT country, n FROM cc WHERE store_id = 1),
   b AS (SELECT country, n FROM cc WHERE store_id = 2)
SELECT a.country, a.n AS store1, b.n AS store2
FROM a LEFT JOIN b ON b.country = a.country
UNION
SELECT b.country, a.n, b.n
FROM a RIGHT JOIN b ON b.country = a.country
ORDER BY country;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| country | store1 | store2 |
|---|---|---|
| Afghanistan | 1.0 | nan |
| Algeria | 2.0 | 1.0 |
| American Samoa | nan | 1.0 |
| Angola | 2.0 | nan |
| Anguilla | nan | 1.0 |
| Argentina | 9.0 | 4.0 |
| Armenia | 1.0 | nan |
| Austria | 2.0 | 1.0 |
| Azerbaijan | nan | 2.0 |
| Bahrain | nan | 1.0 |
| Bangladesh | 2.0 | 1.0 |
| Belarus | 2.0 | nan |
| Bolivia | nan | 2.0 |
| Brazil | 15.0 | 13.0 |
| Brunei | nan | 1.0 |
| Bulgaria | 1.0 | 1.0 |
| Cambodia | nan | 2.0 |
| Cameroon | 1.0 | 1.0 |
| Canada | 3.0 | 2.0 |
| Chad | 1.0 | nan |

> 총 108행 중 상위 20행만 표시

</details>

## 해설

FULL OUTER JOIN = LEFT OUTER JOIN ∪ RIGHT OUTER JOIN (중복 제거). 두 결과를 `UNION` 으로 합칩니다.
`UNION ALL` 을 쓰면 양쪽에 다 있는 국가가 두 번 나오니 주의하세요. 결과에서 한쪽 매장에만 고객이 있는 국가를 확인해 보세요.
