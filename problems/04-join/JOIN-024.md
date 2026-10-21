# JOIN-024. 배우가 출연한 장르 수

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `다중 조인` `COUNT DISTINCT`

## 문제

가장 다양한 장르에 출연한 배우 5명의 `actor_id`, `actor`(이름 성), `categories`(출연 장르 수), `films`(출연 편수) 를 구하세요.
장르 수 내림차순, 출연 편수 내림차순, `actor_id` 순.

**사용 테이블:** `actor`, `film_actor`, `film_category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT a.actor_id,
       CONCAT(a.first_name, ' ', a.last_name) AS actor,
       COUNT(DISTINCT fc.category_id) AS categories,
       COUNT(*) AS films
FROM actor a
JOIN film_actor fa    ON fa.actor_id = a.actor_id
JOIN film_category fc ON fc.film_id  = fa.film_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY categories DESC, films DESC, a.actor_id
LIMIT 5;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| actor_id | actor | categories | films |
|---|---|---|---|
| 107 | GINA DEGENERES | 16 | 42 |
| 13 | UMA WOOD | 16 | 35 |
| 106 | GROUCHO DUNST | 16 | 35 |
| 127 | KEVIN GARLAND | 16 | 33 |
| 139 | EWAN GOODING | 16 | 33 |

> 총 5행

</details>

## 해설

`film_category` 는 영화당 1행이라 팬아웃이 없으므로 `COUNT(*)` 가 곧 출연 편수입니다.
장르가 여러 개인 구조였다면 `COUNT(DISTINCT fa.film_id)` 로 바꿔야 합니다.
