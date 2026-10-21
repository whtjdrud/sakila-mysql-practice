# SQLD-012. 단일행 서브쿼리 vs 다중행 서브쿼리

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `다중행 서브쿼리` `IN` `단일행 연산자`

## 문제

성이 `KILMER` 인 배우들이 출연한 영화의 수를 구하세요. (`KILMER` 성을 가진 배우는 여러 명입니다)

- 출력: `films`

**사용 테이블:** `film_actor`, `actor`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT COUNT(DISTINCT film_id) AS films
FROM film_actor
WHERE actor_id IN (SELECT actor_id FROM actor WHERE last_name = 'KILMER');
```

</details>

<details>
<summary>실행 결과 보기</summary>

| films |
|---|
| 126 |

> 총 1행

</details>

## 해설

**SQLD 빈출**: 서브쿼리가 여러 행을 돌려줄 수 있으면 `=`, `>` 같은 **단일행 연산자**를 쓸 수 없습니다 (`Subquery returns more than 1 row` 오류).
다중행 연산자 `IN`, `ANY`, `ALL`, `EXISTS` 를 써야 합니다. 두 배우가 같은 영화에 나왔을 수 있으므로 `DISTINCT` 도 필요합니다.
