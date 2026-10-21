# JOIN-009. 같은 도시에 사는 고객 쌍

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `SELF JOIN`

## 문제

같은 도시(`city_id`)에 사는 **서로 다른 고객 쌍**을 찾으세요. 같은 쌍이 두 번 나오면 안 됩니다.

- 출력: `city`, `customer_a`, `customer_b`(각각 customer_id, a < b) — `city`, `customer_a`, `customer_b` 순

**사용 테이블:** `customer`, `address`, `city`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT ci.city, c1.customer_id AS customer_a, c2.customer_id AS customer_b
FROM customer c1
JOIN address a1 ON a1.address_id = c1.address_id
JOIN address a2 ON a2.city_id    = a1.city_id
JOIN customer c2 ON c2.address_id = a2.address_id
JOIN city ci     ON ci.city_id    = a1.city_id
WHERE c1.customer_id < c2.customer_id
ORDER BY ci.city, customer_a, customer_b;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| city | customer_a | customer_b |
|---|---|---|
| Aurora | 330 | 537 |
| London | 252 | 512 |

> 총 2행

</details>

## 해설

**셀프 조인**은 같은 테이블을 다른 별칭으로 두 번 사용합니다.
`c1.customer_id < c2.customer_id` 조건이 (A, B)·(B, A) 중복과 자기 자신과의 쌍 (A, A) 을 한 번에 제거합니다. `<>` 를 쓰면 쌍이 두 번 나옵니다.
