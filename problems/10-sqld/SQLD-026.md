# SQLD-026. 논리 연산자 우선순위 (NOT > AND > OR)

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `NOT` `AND` `OR` `우선순위`

## 문제

다음 조건의 결과 행 수를 각각 구해 한 행으로 출력하세요. (`film` 테이블)

- `a`: `NOT rating = 'G' AND rental_rate = 0.99`
- `b`: `NOT (rating = 'G' AND rental_rate = 0.99)`
- `c`: `rating = 'G' OR rating = 'PG' AND rental_rate = 0.99`
- `d`: `(rating = 'G' OR rating = 'PG') AND rental_rate = 0.99`

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT
  (SELECT COUNT(*) FROM film WHERE NOT rating = 'G' AND rental_rate = 0.99)                 AS a,
  (SELECT COUNT(*) FROM film WHERE NOT (rating = 'G' AND rental_rate = 0.99))               AS b,
  (SELECT COUNT(*) FROM film WHERE rating = 'G' OR rating = 'PG' AND rental_rate = 0.99)    AS c,
  (SELECT COUNT(*) FROM film WHERE (rating = 'G' OR rating = 'PG') AND rental_rate = 0.99)  AS d;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| a | b | c | d |
|---|---|---|---|
| 277 | 936 | 240 | 126 |

> 총 1행

</details>

## 해설

우선순위는 **NOT → AND → OR**. `a` 는 `(NOT rating='G') AND ...`, `c` 는 `rating='G' OR (rating='PG' AND ...)` 로 해석됩니다.
a 와 b, c 와 d 의 차이가 곧 괄호의 효과입니다. 시험에서는 "결과 건수가 다른 것은?" 형식으로 자주 출제됩니다.
