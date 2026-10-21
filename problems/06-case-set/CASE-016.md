# CASE-016. 등급별 특별 부록 포함 여부 교차표

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `피벗` `FIND_IN_SET`

## 문제

등급별로 각 특별 부록(`Trailers`, `Commentaries`, `Deleted Scenes`, `Behind the Scenes`)이 포함된 영화 비율(%)을 구하세요.

- 출력: `rating`, `trailers`, `commentaries`, `deleted`, `behind` (모두 소수 1자리) — `rating` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rating,
       ROUND(100 * AVG(FIND_IN_SET('Trailers', special_features) > 0), 1)          AS trailers,
       ROUND(100 * AVG(FIND_IN_SET('Commentaries', special_features) > 0), 1)      AS commentaries,
       ROUND(100 * AVG(FIND_IN_SET('Deleted Scenes', special_features) > 0), 1)    AS deleted,
       ROUND(100 * AVG(FIND_IN_SET('Behind the Scenes', special_features) > 0), 1) AS behind
FROM film
GROUP BY rating
ORDER BY rating;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating | trailers | commentaries | deleted | behind |
|---|---|---|---|---|
| G | 52.8 | 55.1 | 50.6 | 50.6 |
| PG | 54.6 | 55.2 | 54.1 | 54.1 |
| PG-13 | 54.7 | 52.5 | 46.6 | 53.8 |
| R | 53.8 | 48.2 | 48.7 | 53.3 |
| NC-17 | 51.4 | 58.6 | 51.9 | 56.7 |

> 총 5행

</details>

## 해설

한 행에 여러 값이 들어간 컬럼(SET)도 조건부 평균으로 비율 피벗을 만들 수 있습니다.
정규화된 설계라면 `film_feature(film_id, feature)` 같은 별도 테이블이 더 다루기 쉽습니다.
