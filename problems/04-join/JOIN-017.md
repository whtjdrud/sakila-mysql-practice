# JOIN-017. USING 과 NATURAL JOIN

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `USING` `NATURAL JOIN`

## 문제

`USING` 을 사용해 `film` 과 `film_category`, `category` 를 조인하고 `film_id` 1~5번의 `film_id`, `title`, `name`(장르) 을 조회하세요.
`film_id` 순.

**사용 테이블:** `film`, `film_category`, `category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT film_id, title, name
FROM film
JOIN film_category USING (film_id)
JOIN category USING (category_id)
WHERE film_id <= 5
ORDER BY film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title | name |
|---|---|---|
| 1 | ACADEMY DINOSAUR | Documentary |
| 2 | ACE GOLDFINGER | Horror |
| 3 | ADAPTATION HOLES | Documentary |
| 4 | AFFAIR PREJUDICE | Horror |
| 5 | AFRICAN EGG | Family |

> 총 5행

</details>

## 해설

`USING (col)` 은 양쪽에 같은 이름의 컬럼이 있을 때 `ON a.col = b.col` 을 줄여 씁니다. 결과에서 그 컬럼은 하나로 합쳐집니다.
`NATURAL JOIN` 은 **이름이 같은 모든 컬럼**으로 조인하는데, Sakila 는 모든 테이블에 `last_update` 가 있어 의도치 않게 그 컬럼까지 조인 조건이 됩니다. 실무에서는 피하세요.
