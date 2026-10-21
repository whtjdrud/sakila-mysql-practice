# JOIN-021. 모든 매장에 재고가 있는 영화

**유형:** 조인 · **난이도:** ★★★★☆ 고급 · **태그:** `관계 나눗셈` `HAVING`

## 문제

**모든 매장**(현재 2곳)에 재고가 있는 영화의 수를 구하세요. 매장 수를 하드코딩하지 마세요.

- 출력: `films_in_all_stores`

**사용 테이블:** `inventory`, `store`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT COUNT(*) AS films_in_all_stores
FROM (
    SELECT film_id
    FROM inventory
    GROUP BY film_id
    HAVING COUNT(DISTINCT store_id) = (SELECT COUNT(*) FROM store)
) t;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| films_in_all_stores |
|---|
| 563 |

> 총 1행

</details>

## 해설

"모든 X 에 대해 Y 인 것" 을 찾는 것을 **관계 나눗셈(relational division)** 이라 합니다.
`HAVING COUNT(DISTINCT ...) = (전체 개수)` 패턴이 가장 직관적이고, `NOT EXISTS` 이중 부정으로도 풀 수 있습니다 (SUB 유형 참고).
