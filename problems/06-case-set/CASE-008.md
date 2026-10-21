# CASE-008. 배우이면서 고객인 이름

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `INTERSECT`

## 문제

배우와 고객 **양쪽에 모두 존재하는** 이름(`first_name`, `last_name` 조합)을 `last_name`, `first_name` 순으로 조회하세요.

**사용 테이블:** `actor`, `customer`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT first_name, last_name FROM actor
INTERSECT
SELECT first_name, last_name FROM customer
ORDER BY last_name, first_name;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| first_name | last_name |
|---|---|
| JENNIFER | DAVIS |

> 총 1행

</details>

## 해설

`INTERSECT`(교집합)와 `EXCEPT`(차집합)는 MySQL **8.0.31** 부터 지원됩니다. 이전 버전에서는 `IN`/`EXISTS` 로 풀어야 합니다.
집합 연산은 NULL 끼리도 **같은 값으로 취급**한다는 점이 `=` 비교와 다릅니다.
