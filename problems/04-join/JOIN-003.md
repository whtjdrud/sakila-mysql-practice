# JOIN-003. 영화별 출연 배우

**유형:** 조인 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `N:M 관계` `연결 테이블`

## 문제

영화 `ACADEMY DINOSAUR` 에 출연한 배우의 `first_name`, `last_name` 을 `last_name`, `first_name` 순으로 조회하세요.

**사용 테이블:** `film`, `film_actor`, `actor`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT a.first_name, a.last_name
FROM film f
JOIN film_actor fa ON fa.film_id  = f.film_id
JOIN actor a       ON a.actor_id  = fa.actor_id
WHERE f.title = 'ACADEMY DINOSAUR'
ORDER BY a.last_name, a.first_name;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| first_name | last_name |
|---|---|
| JOHNNY | CAGE |
| ROCK | DUKAKIS |
| CHRISTIAN | GABLE |
| PENELOPE | GUINESS |
| MARY | KEITEL |
| OPRAH | KILMER |
| WARREN | NOLTE |
| SANDRA | PECK |
| MENA | TEMPLE |
| LUCILLE | TRACY |

> 총 10행

</details>

## 해설

영화와 배우는 **다대다(N:M)** 관계라서 `film_actor` 연결 테이블을 거쳐야 합니다.
