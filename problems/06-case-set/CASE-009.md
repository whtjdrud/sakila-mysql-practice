# CASE-009. 대여는 있지만 2006년엔 없는 고객

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `EXCEPT`

## 문제

2005년 8월에는 대여했지만 2006년에는 대여하지 않은 고객의 수를 `EXCEPT` 로 구하세요.

- 출력: `customers`

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT COUNT(*) AS customers
FROM (
    SELECT customer_id FROM rental
    WHERE rental_date >= '2005-08-01' AND rental_date < '2005-09-01'
    EXCEPT
    SELECT customer_id FROM rental
    WHERE rental_date >= '2006-01-01'
) t;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| customers |
|---|
| 441 |

> 총 1행

</details>

## 해설

`A EXCEPT B` 는 A 에는 있고 B 에는 없는 행입니다. 결과는 자동으로 중복이 제거됩니다 (`EXCEPT ALL` 은 중복 유지).
같은 문제를 `NOT EXISTS` 로도 풀어 보세요.
