# JOIN-005. 가장 많이 대여된 영화 TOP 10

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `다중 조인` `GROUP BY` `LIMIT 함정`

## 문제

전체 기간 동안 대여 횟수가 가장 많은 영화 10편을 구하세요.

- 출력: `title`, `rating`, `rental_count`
- 대여 횟수 내림차순, 같으면 제목 오름차순

**사용 테이블:** `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.title,
       f.rating,
       COUNT(r.rental_id) AS rental_count
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
GROUP BY f.film_id, f.title, f.rating
ORDER BY rental_count DESC, f.title
LIMIT 10;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| title | rating | rental_count |
|---|---|---|
| BUCKET BROTHERHOOD | PG | 34 |
| ROCKETEER MOTHER | PG-13 | 33 |
| FORWARD TEMPLE | NC-17 | 32 |
| GRIT CLOCKWORK | PG | 32 |
| JUGGLER HARDLY | PG-13 | 32 |
| RIDGEMONT SUBMARINE | PG-13 | 32 |
| SCALAWAG DUCK | NC-17 | 32 |
| APACHE DIVINE | NC-17 | 31 |
| GOODFELLAS SALUTE | PG | 31 |
| HOBBIT ALIEN | PG-13 | 31 |

> 총 10행

</details>

## 해설

- 1위는 **BUCKET BROTHERHOOD(34회)**, 2위 ROCKETEER MOTHER(33회)입니다.
- ⚠️ 8~10위는 모두 31회인데, 실제로 **31회 이상 대여된 영화는 16편**입니다. 31회인 영화 일부는 제목 순서 때문에 잘려 나갔습니다.
- "상위 10위까지"를 공정하게 뽑으려면 `RANK() OVER (ORDER BY COUNT(*) DESC)` 로 순위를 매긴 뒤 `rnk <= 10` 으로 거르세요. (WIN 유형 참고)
