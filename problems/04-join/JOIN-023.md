# JOIN-023. 최근 대여 영화의 다른 출연작

**유형:** 조인 · **난이도:** ★★★★☆ 고급 · **태그:** `다중 조인` `추천` `DISTINCT`

## 문제

고객 1번이 **가장 최근에 빌린 영화**의 출연 배우들이 출연한 **다른 영화** 중, 고객 1번이 한 번도 빌린 적 없는 영화를 추천하세요.

- 출력: `film_id`, `title`, `shared_actors`(최근 영화와 겹치는 배우 수)
- 겹치는 배우 수 내림차순, `film_id` 순으로 상위 10편

**사용 테이블:** `rental`, `inventory`, `film_actor`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.film_id, f.title, COUNT(DISTINCT fa2.actor_id) AS shared_actors
FROM (
    SELECT i.film_id
    FROM rental r
    JOIN inventory i ON i.inventory_id = r.inventory_id
    WHERE r.customer_id = 1
    ORDER BY r.rental_date DESC, r.rental_id DESC
    LIMIT 1
) last_film
JOIN film_actor fa1 ON fa1.film_id  = last_film.film_id
JOIN film_actor fa2 ON fa2.actor_id = fa1.actor_id
                   AND fa2.film_id <> last_film.film_id
JOIN film f ON f.film_id = fa2.film_id
WHERE NOT EXISTS (
    SELECT 1
    FROM rental r2
    JOIN inventory i2 ON i2.inventory_id = r2.inventory_id
    WHERE r2.customer_id = 1 AND i2.film_id = f.film_id
)
GROUP BY f.film_id, f.title
ORDER BY shared_actors DESC, f.film_id
LIMIT 10;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title | shared_actors |
|---|---|---|
| 892 | TITANIC BOONDOCK | 2 |
| 19 | AMADEUS HOLY | 1 |
| 29 | ANTITRUST TOMATOES | 1 |
| 39 | ARMAGEDDON LOST | 1 |
| 40 | ARMY FLINTSTONES | 1 |
| 53 | BANG KWAI | 1 |
| 59 | BEAR GRACELAND | 1 |
| 60 | BEAST HUNCHBACK | 1 |
| 112 | CALENDAR GUNFIGHT | 1 |
| 136 | CHAPLIN LICENSE | 1 |

> 총 10행

</details>

## 해설

"이 영화를 본 사람에게 같은 배우의 다른 영화를 추천" 하는 간단한 **콘텐츠 기반 추천**입니다.
파생 테이블(최근 영화) → 셀프 조인(같은 배우) → 안티 조인(이미 본 영화 제외) → 점수 정렬 순서로 조립했습니다.
