# SQLD-013. 다중 컬럼 서브쿼리

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `다중 컬럼 서브쿼리` `그룹별 최댓값`

## 문제

등급별로 상영 시간이 **가장 긴** 영화를 `(rating, length) IN (SELECT ...)` 형식의 다중 컬럼 서브쿼리로 구하세요.

- 출력: `rating`, `title`, `length` — `rating`, `title` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rating, title, length
FROM film
WHERE (rating, length) IN (SELECT rating, MAX(length) FROM film GROUP BY rating)
ORDER BY rating, title;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating | title | length |
|---|---|---|
| G | CONTROL ANTHEM | 185 |
| G | DARN FORRESTER | 185 |
| G | MUSCLE BRIGHT | 185 |
| PG | WORST BANGER | 185 |
| PG-13 | CHICAGO NORTH | 185 |
| PG-13 | GANGS PRIDE | 185 |
| PG-13 | POND SEATTLE | 185 |
| R | HOME PITY | 185 |
| R | SOLDIERS EVOLUTION | 185 |
| R | SWEET BROTHERHOOD | 185 |
| NC-17 | CRYSTAL BREAKING | 184 |
| NC-17 | KING EVOLUTION | 184 |
| NC-17 | SONS INTERVIEW | 184 |
| NC-17 | SORORITY QUEEN | 184 |

> 총 14행

</details>

## 해설

다중 컬럼 서브쿼리는 Oracle·MySQL 모두 지원하지만 **SQL Server 는 지원하지 않습니다** (시험 단골 비교 문항).
`WHERE length IN (SELECT MAX(length) ... GROUP BY rating)` 처럼 한 컬럼만 비교하면, 다른 등급의 최댓값과 우연히 같은 영화까지 섞입니다.
