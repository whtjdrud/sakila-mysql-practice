# CASE-002. 등급을 한국어로

**유형:** 조건식·집합 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `단순 CASE`

## 문제

등급별 영화 수를 구하되 등급을 한국 기준 설명으로 바꿔 표시하세요.

| rating | 설명 |
|---|---|
| G | 전체관람가 |
| PG, PG-13 | 12세 이상 |
| R | 15세 이상 |
| NC-17 | 청소년 관람불가 |

- 출력: `rating_kr`, `films` — `films` 내림차순, `rating_kr` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT CASE rating
         WHEN 'G'     THEN '전체관람가'
         WHEN 'PG'    THEN '12세 이상'
         WHEN 'PG-13' THEN '12세 이상'
         WHEN 'R'     THEN '15세 이상'
         WHEN 'NC-17' THEN '청소년 관람불가'
       END AS rating_kr,
       COUNT(*) AS films
FROM film
GROUP BY rating_kr
ORDER BY films DESC, rating_kr;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating_kr | films |
|---|---|
| 12세 이상 | 417 |
| 청소년 관람불가 | 210 |
| 15세 이상 | 195 |
| 전체관람가 | 178 |

> 총 4행

</details>

## 해설

`CASE 컬럼 WHEN 값 THEN ...` 형태를 **단순 CASE** 라 합니다. 등호 비교만 할 때 간결합니다.
`ELSE` 를 생략하면 어느 조건에도 맞지 않는 값은 NULL 이 됩니다.
