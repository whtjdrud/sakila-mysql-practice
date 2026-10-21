# CASE-013. 요일 × 시간대 히트맵

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `피벗` `CASE` `시간대`

## 문제

대여를 요일(행)과 시간대(열)로 교차 집계하세요. 시간대: `새벽`(0~5시), `오전`(6~11시), `오후`(12~17시), `저녁`(18~23시).

- 출력: `dow`(1=일 … 7=토), `day_name`, `dawn`, `morning`, `afternoon`, `evening` — `dow` 순

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT DAYOFWEEK(rental_date) AS dow,
       DAYNAME(rental_date)   AS day_name,
       SUM(HOUR(rental_date) BETWEEN 0  AND 5)  AS dawn,
       SUM(HOUR(rental_date) BETWEEN 6  AND 11) AS morning,
       SUM(HOUR(rental_date) BETWEEN 12 AND 17) AS afternoon,
       SUM(HOUR(rental_date) BETWEEN 18 AND 23) AS evening
FROM rental
GROUP BY dow, day_name
ORDER BY dow;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| dow | day_name | dawn | morning | afternoon | evening |
|---|---|---|---|---|---|
| 1 | Sunday | 580 | 586 | 586 | 568 |
| 2 | Monday | 597 | 552 | 531 | 567 |
| 3 | Tuesday | 619 | 543 | 748 | 553 |
| 4 | Wednesday | 551 | 528 | 568 | 584 |
| 5 | Thursday | 523 | 586 | 551 | 540 |
| 6 | Friday | 549 | 620 | 532 | 571 |
| 7 | Saturday | 567 | 583 | 599 | 562 |

> 총 7행

</details>

## 해설

시각화 도구의 히트맵 입력 데이터를 SQL 로 바로 만드는 패턴입니다. 행 합계가 요일별 대여 수와 같은지 검산해 보세요.
