# JOIN-001. 영화와 언어

**유형:** 조인 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `INNER JOIN`

## 문제

`film_id` 1~5번 영화의 `title` 과 언어 이름 `language` 를 조회하세요. `film_id` 순.

**사용 테이블:** `film`, `language`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.film_id, f.title, l.name AS language
FROM film f
JOIN language l ON l.language_id = f.language_id
WHERE f.film_id <= 5
ORDER BY f.film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title | language |
|---|---|---|
| 1 | ACADEMY DINOSAUR | English |
| 2 | ACE GOLDFINGER | English |
| 3 | ADAPTATION HOLES | English |
| 4 | AFFAIR PREJUDICE | English |
| 5 | AFRICAN EGG | English |

> 총 5행

</details>

## 해설

`JOIN` 은 `INNER JOIN` 의 줄임말입니다. 두 테이블에서 **조건이 맞는 행끼리만** 결합합니다.
테이블 별칭(`f`, `l`)을 쓰면 쿼리가 짧아지고, 같은 이름의 컬럼을 구분할 수 있습니다.
