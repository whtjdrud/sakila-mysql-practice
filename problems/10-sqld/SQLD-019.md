# SQLD-019. 윈도우 프레임 ROWS vs RANGE

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `ROWS` `RANGE` `윈도우 프레임` `동점`

## 문제

`film_id` 1~12번 영화를 대여료 순으로 정렬해 대여료 누적합을 두 가지 프레임으로 구하세요.

- `rows_sum`: `ORDER BY rental_rate, film_id` + `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
- `range_sum`: `ORDER BY rental_rate` (동점 그대로) + `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

출력: `film_id`, `rental_rate`, `rows_sum`, `range_sum` — `rental_rate`, `film_id` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT film_id, rental_rate, rows_sum, range_sum
FROM (
    SELECT film_id, rental_rate,
           SUM(rental_rate) OVER (ORDER BY rental_rate, film_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_sum,
           SUM(rental_rate) OVER (ORDER BY rental_rate RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_sum
    FROM film
    WHERE film_id <= 12
) t
ORDER BY rental_rate, film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | rental_rate | rows_sum | range_sum |
|---|---|---|---|
| 1 | 0.99 | 0.99 | 2.97 |
| 11 | 0.99 | 1.98 | 2.97 |
| 12 | 0.99 | 2.97 | 2.97 |
| 3 | 2.99 | 5.96 | 17.92 |
| 4 | 2.99 | 8.95 | 17.92 |
| 5 | 2.99 | 11.94 | 17.92 |
| 6 | 2.99 | 14.93 | 17.92 |
| 9 | 2.99 | 17.92 | 17.92 |
| 2 | 4.99 | 22.91 | 37.88 |
| 7 | 4.99 | 27.90 | 37.88 |
| 8 | 4.99 | 32.89 | 37.88 |
| 10 | 4.99 | 37.88 | 37.88 |

> 총 12행

</details>

## 해설

`RANGE` 는 정렬 값이 **같은 행들을 한 묶음**으로 보므로 동점 행들의 누적합이 모두 같습니다. `ROWS` 는 물리적 행 하나씩 더합니다.
**SQLD 빈출**: `ORDER BY` 만 쓰고 프레임을 생략하면 기본값은 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` 입니다.
ROWS 쪽에 `film_id` 를 추가한 이유: 동점 안에서 어느 행을 먼저 더할지는 DB 마음이라, 정렬 키를 끝까지 정해야 결과가 매번 같습니다.
