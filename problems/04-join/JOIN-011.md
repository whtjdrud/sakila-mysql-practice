# JOIN-011. 매장 관리자 정보

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `다중 조인` `역할이 다른 조인`

## 문제

각 매장의 `store_id`, 관리자 이름 `manager`, 매장 주소 `store_address`, 도시 `city` 를 조회하세요. `store_id` 순.

**사용 테이블:** `store`, `staff`, `address`, `city`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT st.store_id,
       CONCAT(sf.first_name, ' ', sf.last_name) AS manager,
       a.address AS store_address,
       ci.city
FROM store st
JOIN staff sf  ON sf.staff_id  = st.manager_staff_id
JOIN address a ON a.address_id = st.address_id
JOIN city ci   ON ci.city_id   = a.city_id
ORDER BY st.store_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store_id | manager | store_address | city |
|---|---|---|---|
| 1 | Mike Hillyer | 47 MySakila Drive | Lethbridge |
| 2 | Jon Stephens | 28 MySQL Boulevard | Woodridge |

> 총 2행

</details>

## 해설

`store` 와 `staff` 는 두 방향으로 연결됩니다: 매장의 관리자(`store.manager_staff_id`)와 직원의 소속 매장(`staff.store_id`).
어떤 관계를 따라 조인하는지 **ON 조건으로 명확히** 해야 합니다.
