# CASE-017. 언피벗 (열을 행으로)

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `UNION ALL` `언피벗`

## 문제

`film_id` 1~3번 영화의 `rental_rate`, `replacement_cost`, `length` 세 값을 **세로로** 펼치세요.

- 출력: `film_id`, `metric`(컬럼명), `value` — `film_id`, `metric` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT film_id, 'length' AS metric, length AS value FROM film WHERE film_id <= 3
UNION ALL
SELECT film_id, 'rental_rate', rental_rate FROM film WHERE film_id <= 3
UNION ALL
SELECT film_id, 'replacement_cost', replacement_cost FROM film WHERE film_id <= 3
ORDER BY film_id, metric;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | metric | value |
|---|---|---|
| 1 | length | 86.00 |
| 1 | rental_rate | 0.99 |
| 1 | replacement_cost | 20.99 |
| 2 | length | 48.00 |
| 2 | rental_rate | 4.99 |
| 2 | replacement_cost | 12.99 |
| 3 | length | 50.00 |
| 3 | rental_rate | 2.99 |
| 3 | replacement_cost | 18.99 |

> 총 9행

</details>

## 해설

피벗의 반대인 **언피벗**은 UNION ALL 로 열마다 SELECT 를 붙여 만듭니다. 차트 도구나 롱 포맷 데이터가 필요할 때 씁니다.
UNION 결과 컬럼의 타입은 모든 SELECT 를 아우르는 타입으로 정해집니다(여기서는 DECIMAL).
