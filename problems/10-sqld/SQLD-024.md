# SQLD-024. 집계 함수 중첩 (MAX(COUNT(*)))

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `집계 중첩` `인라인 뷰`

## 문제

등급별 영화 수 중 **가장 큰 값**을 구하세요. Oracle 에서는 `SELECT MAX(COUNT(*)) FROM film GROUP BY rating` 이 가능하지만 MySQL 은 불가능합니다.

- 출력: `max_films`

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT MAX(films) AS max_films
FROM (SELECT rating, COUNT(*) AS films FROM film GROUP BY rating) t;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| max_films |
|---|
| 223 |

> 총 1행

</details>

## 해설

Oracle 은 GROUP BY 가 있을 때 집계 함수를 **한 번** 중첩할 수 있습니다(`MAX(COUNT(*))`). MySQL·표준 SQL 은 인라인 뷰로 감싸야 합니다.
중첩 집계의 결과는 1행이므로, SELECT 목록에 `rating` 같은 그룹 컬럼을 함께 쓸 수 없다는 것도 시험 포인트입니다.
