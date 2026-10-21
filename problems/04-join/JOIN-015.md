# JOIN-015. 비등가 조인으로 등급 매기기

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `비등가 조인` `BETWEEN JOIN`

## 문제

아래 가격 등급표를 **파생 테이블**로 만들어, 영화를 `replacement_cost` 에 따라 등급별로 집계하세요.

| tier | 최소 | 최대 |
|---|---|---|
| 저가 | 0 | 14.99 |
| 중가 | 15 | 22.99 |
| 고가 | 23 | 99.99 |

- 출력: `tier`, `films`, `avg_cost`(소수 2자리) — 최소값 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT t.tier, COUNT(*) AS films, ROUND(AVG(f.replacement_cost), 2) AS avg_cost
FROM film f
JOIN (
    SELECT '저가' AS tier, 0 AS lo, 14.99 AS hi
    UNION ALL SELECT '중가', 15, 22.99
    UNION ALL SELECT '고가', 23, 99.99
) t ON f.replacement_cost BETWEEN t.lo AND t.hi
GROUP BY t.tier, t.lo
ORDER BY t.lo;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| tier | films | avg_cost |
|---|---|---|
| 저가 | 300 | 12.61 |
| 중가 | 381 | 19.82 |
| 고가 | 319 | 27.12 |

> 총 3행

</details>

## 해설

조인 조건이 `=` 가 아닌 범위(`BETWEEN`, `<`, `>`)인 것을 **비등가 조인**이라 합니다. 등급표·환율표·세율표 매핑에 씁니다.
`UNION ALL` 로 작은 기준표를 즉석에서 만들 수 있습니다 (MySQL 8.0.19+ 는 `VALUES ROW(...)` 문법도 지원).
