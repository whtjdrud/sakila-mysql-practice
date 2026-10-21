# JOIN-010. 함께 출연한 배우 쌍

**유형:** 조인 · **난이도:** ★★★★☆ 고급 · **태그:** `SELF JOIN` `GROUP BY` `공동 출연`

## 문제

가장 많은 영화에 **함께 출연한** 배우 쌍 5개를 구하세요.

- 출력: `actor_a`, `actor_b`(각각 "이름 성"), `films_together`
- 함께 출연 편수 내림차순, 그다음 두 배우의 actor_id 순 (a 의 id < b 의 id)

**사용 테이블:** `film_actor`, `actor`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT CONCAT(a1.first_name, ' ', a1.last_name) AS actor_a,
       CONCAT(a2.first_name, ' ', a2.last_name) AS actor_b,
       COUNT(*) AS films_together
FROM film_actor fa1
JOIN film_actor fa2 ON fa2.film_id = fa1.film_id
                   AND fa2.actor_id > fa1.actor_id
JOIN actor a1 ON a1.actor_id = fa1.actor_id
JOIN actor a2 ON a2.actor_id = fa2.actor_id
GROUP BY fa1.actor_id, fa2.actor_id, a1.first_name, a1.last_name, a2.first_name, a2.last_name
ORDER BY films_together DESC, fa1.actor_id, fa2.actor_id
LIMIT 5;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| actor_a | actor_b | films_together |
|---|---|---|
| JULIA MCQUEEN | HENRY BERRY | 7 |
| CUBA OLIVIER | MARY KEITEL | 6 |
| KIRSTEN PALTROW | WARREN NOLTE | 6 |
| VAL BOLGER | ROCK DUKAKIS | 6 |
| BEN WILLIS | HARVEY HOPE | 6 |

> 총 5행

</details>

## 해설

연결 테이블을 셀프 조인하면 "같은 영화에 나온 두 배우" 를 만들 수 있습니다. 추천 시스템의 **동시 출현(co-occurrence)** 분석과 같은 원리입니다.
조인 결과 행 수가 영화당 (배우 수 × 배우 수 / 2) 로 늘어나므로 대용량에서는 비용이 큽니다.
