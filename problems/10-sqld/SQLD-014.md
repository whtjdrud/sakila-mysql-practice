# SQLD-014. ORDER BY 절의 스칼라 서브쿼리

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `스칼라 서브쿼리` `ORDER BY`

## 문제

고객 1~20번을 **가장 최근 대여일이 늦은 순**으로 정렬해 상위 5명의 `customer_id`, `first_name`, `last_name` 을 조회하세요.
최근 대여일은 SELECT 목록에 넣지 말고 **ORDER BY 절의 스칼라 서브쿼리**로만 사용하세요. 같으면 `customer_id` 순.

**사용 테이블:** `customer`, `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT c.customer_id, c.first_name, c.last_name
FROM customer c
WHERE c.customer_id <= 20
ORDER BY (SELECT MAX(r.rental_date) FROM rental r WHERE r.customer_id = c.customer_id) DESC,
         c.customer_id
LIMIT 5;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| customer_id | first_name | last_name |
|---|---|---|
| 5 | ELIZABETH | BROWN |
| 9 | MARGARET | MOORE |
| 11 | LISA | ANDERSON |
| 14 | BETTY | WHITE |
| 15 | HELEN | HARRIS |

> 총 5행

</details>

## 해설

스칼라 서브쿼리는 SELECT 절뿐 아니라 **ORDER BY, WHERE, HAVING, CASE** 등 값이 올 수 있는 거의 모든 곳에 쓸 수 있습니다.
단, **GROUP BY 절에는 쓸 수 없다**(Oracle 기준)는 것이 시험에 나옵니다.
