# JOIN-002. 고객 주소 조회

**유형:** 조인 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `INNER JOIN` `다중 조인`

## 문제

고객 1~5번의 `customer_id`, 이름 `name`(이름 성), `address`, `city`, `country` 를 조회하세요. `customer_id` 순.

**사용 테이블:** `customer`, `address`, `city`, `country`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT c.customer_id,
       CONCAT(c.first_name, ' ', c.last_name) AS name,
       a.address, ci.city, co.country
FROM customer c
JOIN address a  ON a.address_id  = c.address_id
JOIN city ci    ON ci.city_id    = a.city_id
JOIN country co ON co.country_id = ci.country_id
WHERE c.customer_id <= 5
ORDER BY c.customer_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| customer_id | name | address | city | country |
|---|---|---|---|---|
| 1 | MARY SMITH | 1913 Hanoi Way | Sasebo | Japan |
| 2 | PATRICIA JOHNSON | 1121 Loja Avenue | San Bernardino | United States |
| 3 | LINDA WILLIAMS | 692 Joliet Street | Athenai | Greece |
| 4 | BARBARA JONES | 1566 Inegl Manor | Myingyan | Myanmar |
| 5 | ELIZABETH BROWN | 53 Idfu Parkway | Nantou | Taiwan |

> 총 5행

</details>

## 해설

조인은 사슬처럼 이어집니다. 각 `ON` 조건이 **FK → PK** 관계를 따라가는지 확인하면 잘못된 조인을 막을 수 있습니다.
