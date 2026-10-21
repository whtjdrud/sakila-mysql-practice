# CASE-007. UNION 과 UNION ALL 의 차이

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `UNION` `UNION ALL` `중복 제거`

## 문제

배우의 이름(`first_name`)과 고객의 이름(`first_name`)을 합친 목록의 개수를 두 가지로 구하세요.

- `union_all_cnt`: UNION ALL 결과 행 수
- `union_cnt`: UNION 결과 행 수

**사용 테이블:** `actor`, `customer`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT
  (SELECT COUNT(*) FROM (SELECT first_name FROM actor UNION ALL SELECT first_name FROM customer) a) AS union_all_cnt,
  (SELECT COUNT(*) FROM (SELECT first_name FROM actor UNION     SELECT first_name FROM customer) u) AS union_cnt;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| union_all_cnt | union_cnt |
|---|---|
| 799 | 647 |

> 총 1행

</details>

## 해설

`UNION` 은 **중복을 제거**(내부적으로 정렬/해시)하므로 느리고, `UNION ALL` 은 그대로 붙여 빠릅니다.
`UNION` 은 두 집합 사이의 중복뿐 아니라 **한쪽 안의 중복**도 제거한다는 점에 주의하세요. 중복 제거가 필요 없다면 항상 UNION ALL 을 쓰세요.
