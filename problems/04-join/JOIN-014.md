# JOIN-014. 같은 날 같은 영화를 빌린 고객 쌍

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `SELF JOIN` `다중 조건 조인`

## 문제

**2005년 5월** 중 **같은 날짜**에 **같은 영화**(재고는 달라도 됨)를 빌린 서로 다른 두 고객 쌍을 찾으세요.

- 출력: `rental_day`, `title`, `customer_a`, `customer_b` (a < b)
- `rental_day`, `title`, `customer_a`, `customer_b` 순

**사용 테이블:** `rental`, `inventory`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT DISTINCT a.rental_day, f.title,
       a.customer_id AS customer_a, b.customer_id AS customer_b
FROM (
    SELECT DATE(r.rental_date) AS rental_day, i.film_id, r.customer_id
    FROM rental r
    JOIN inventory i ON i.inventory_id = r.inventory_id
    WHERE r.rental_date >= '2005-05-01' AND r.rental_date < '2005-06-01'
) a
JOIN (
    SELECT DATE(r.rental_date) AS rental_day, i.film_id, r.customer_id
    FROM rental r
    JOIN inventory i ON i.inventory_id = r.inventory_id
    WHERE r.rental_date >= '2005-05-01' AND r.rental_date < '2005-06-01'
) b ON b.film_id     = a.film_id
   AND b.rental_day  = a.rental_day
   AND b.customer_id > a.customer_id
JOIN film f ON f.film_id = a.film_id
ORDER BY a.rental_day, f.title, customer_a, customer_b;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rental_day | title | customer_a | customer_b |
|---|---|---|---|
| 2005-05-25 | BINGO TALENTED | 257 | 470 |
| 2005-05-25 | BORROWERS BEDAZZLED | 237 | 535 |
| 2005-05-25 | BUCKET BROTHERHOOD | 131 | 414 |
| 2005-05-25 | ENEMY ODDS | 263 | 484 |
| 2005-05-25 | JUMPING WRATH | 222 | 266 |
| 2005-05-25 | PELICAN COMFORTS | 319 | 323 |
| 2005-05-25 | THIEF PELICAN | 135 | 232 |
| 2005-05-25 | WHALE BIKINI | 142 | 438 |
| 2005-05-26 | AGENT TRUMAN | 391 | 482 |
| 2005-05-26 | CALENDAR GUNFIGHT | 211 | 564 |
| 2005-05-26 | DOOM DANCING | 58 | 319 |
| 2005-05-26 | GANGS PRIDE | 48 | 193 |
| 2005-05-26 | GRAFFITI LOVE | 75 | 133 |
| 2005-05-26 | GRAFFITI LOVE | 75 | 345 |
| 2005-05-26 | GRAFFITI LOVE | 133 | 345 |
| 2005-05-26 | HALF OUTFIELD | 391 | 468 |
| 2005-05-26 | HEDWIG ALTER | 167 | 437 |
| 2005-05-26 | MASSACRE USUAL | 19 | 373 |
| 2005-05-26 | MOVIE SHAKESPEARE | 75 | 369 |
| 2005-05-26 | NETWORK PEAK | 201 | 240 |

> 총 94행 중 상위 20행만 표시

</details>

## 해설

조인 조건은 여러 개를 `AND` 로 묶을 수 있습니다. 여기서는 "같은 영화 + 같은 날 + 다른 고객(a < b)" 세 조건입니다.
재고(DVD)가 같을 필요는 없으므로 대여마다 `film_id` 와 날짜를 먼저 뽑은 **파생 테이블끼리** 셀프 조인했습니다.
`rental` 을 직접 셀프 조인하면서 `DATE(r2.rental_date) = DATE(r1.rental_date)` 를 조건으로 걸면 인덱스를 못 타서 수 초가 걸립니다.
**셀프 조인은 행 수의 제곱으로 커지므로** 양쪽을 먼저 줄여 두는 것이 핵심입니다.
같은 고객이 같은 날 같은 영화를 두 장 빌린 경우 중복 쌍이 생기므로 `DISTINCT` 로 제거했습니다.
