# SQLD-003. ORDER BY 위치 번호와 별칭

**유형:** SQLD 유형 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `ORDER BY` `위치 번호` `별칭`

## 문제

등급별 영화 수와 평균 대여료(소수 2자리)를 구하고, **SELECT 목록의 위치 번호**를 이용해
영화 수(2번째 컬럼) 내림차순, 등급(1번째 컬럼) 오름차순으로 정렬하세요.

- 출력: `rating`, `films`, `avg_rate`

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rating, COUNT(*) AS films, ROUND(AVG(rental_rate), 2) AS avg_rate
FROM film
GROUP BY rating
ORDER BY 2 DESC, 1;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rating | films | avg_rate |
|---|---|---|
| PG-13 | 223 | 3.03 |
| NC-17 | 210 | 2.97 |
| R | 195 | 2.94 |
| PG | 194 | 3.05 |
| G | 178 | 2.89 |

> 총 5행

</details>

## 해설

**SQLD 빈출**: ORDER BY 에는 컬럼명, **별칭**, **SELECT 목록 위치 번호**를 모두 쓸 수 있습니다 (섞어 써도 됨).
실행 순서상 ORDER BY 가 SELECT 다음이라 별칭이 가능하지만, WHERE·GROUP BY 에서는 (표준상) 별칭을 쓸 수 없습니다.
위치 번호는 SELECT 목록이 바뀌면 의미가 바뀌므로 실무 코드에서는 권장되지 않습니다.
