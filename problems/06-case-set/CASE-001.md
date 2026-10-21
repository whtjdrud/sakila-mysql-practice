# CASE-001. 상영 시간 분류

**유형:** 조건식·집합 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `CASE WHEN`

## 문제

영화를 상영 시간에 따라 `단편`(60분 미만), `보통`(60~119분), `장편`(120분 이상)으로 분류하고 분류별 편수를 구하세요.

- 출력: `length_type`, `films` — 단편 → 보통 → 장편 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT CASE WHEN length < 60  THEN '단편'
            WHEN length < 120 THEN '보통'
            ELSE '장편' END AS length_type,
       COUNT(*) AS films
FROM film
GROUP BY length_type
ORDER BY MIN(length);
```

</details>

<details>
<summary>실행 결과 보기</summary>

| length_type | films |
|---|---|
| 단편 | 96 |
| 보통 | 438 |
| 장편 | 466 |

> 총 3행

</details>

## 해설

`CASE` 는 **위에서부터 처음 참인 조건**의 값을 돌려줍니다. 그래서 두 번째 조건에 `length >= 60 AND` 를 다시 쓸 필요가 없습니다.
정렬 순서를 따로 지정하는 대신 `ORDER BY MIN(length)` 로 그룹의 자연스러운 순서를 이용했습니다.
