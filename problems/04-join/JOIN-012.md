# JOIN-012. 매장 주소와 고객 주소가 같은 나라

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `다중 조인` `같은 테이블 두 번`

## 문제

고객이 사는 국가와 그 고객이 등록된 매장(`customer.store_id`)이 있는 국가가 **같은** 고객의 수를 매장별로 구하세요.

- 출력: `store_id`, `store_country`, `local_customers` — `store_id` 순

**사용 테이블:** `customer`, `store`, `address`, `city`, `country`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT st.store_id, sco.country AS store_country, COUNT(*) AS local_customers
FROM customer c
JOIN address ca  ON ca.address_id = c.address_id
JOIN city cci    ON cci.city_id   = ca.city_id
JOIN store st    ON st.store_id   = c.store_id
JOIN address sa  ON sa.address_id = st.address_id
JOIN city sci    ON sci.city_id   = sa.city_id
JOIN country sco ON sco.country_id = sci.country_id
WHERE cci.country_id = sci.country_id
GROUP BY st.store_id, sco.country
ORDER BY st.store_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store_id | store_country | local_customers |
|---|---|---|
| 1 | Canada | 3 |

> 총 1행

</details>

## 해설

같은 테이블(`address`, `city`)을 **역할별로 다른 별칭**(고객용 `ca`, 매장용 `sa`)으로 두 번 조인했습니다.
별칭 이름에 역할을 담으면 긴 조인도 읽기 쉬워집니다.
