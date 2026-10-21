# SQLD-017. GROUPING SETS 흉내내기

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `GROUPING SETS` `UNION ALL`

## 문제

`GROUPING SETS ((rating), (rental_rate))` 와 같은 결과를 만드세요. 등급별 영화 수와 대여료별 영화 수를 **한 결과**에 담습니다.

- 출력: `rating`(대여료 그룹 행에서는 NULL), `rental_rate`(등급 그룹 행에서는 NULL), `films`
- 등급 그룹이 먼저(등급 순), 그다음 대여료 그룹(대여료 순)

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rating, NULL AS rental_rate, COUNT(*) AS films
FROM film GROUP BY rating
UNION ALL
SELECT NULL, rental_rate, COUNT(*)
FROM film GROUP BY rental_rate
ORDER BY rating IS NULL, rating, rental_rate;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating | rental_rate | films |
|---|---|---|
| G | NULL | 178 |
| PG | NULL | 194 |
| PG-13 | NULL | 223 |
| R | NULL | 195 |
| NC-17 | NULL | 210 |
| nan | 0.99 | 341 |
| nan | 2.99 | 323 |
| nan | 4.99 | 336 |

> 총 8행

</details>

## 해설

`GROUPING SETS` 는 **나열한 그룹만** 따로 집계해 합친 것입니다 (ROLLUP 과 달리 총계가 자동으로 생기지 않음, `()` 를 넣어야 총계).
`GROUPING SETS ((a), (b))` = `GROUP BY a UNION ALL GROUP BY b`. 인자 순서가 바뀌어도 결과 집합은 같다는 것도 시험 포인트입니다.
