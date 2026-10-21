# SQLD-008. ROWNUM 과 Top-N 의 함정

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `ROWNUM` `Top-N` `ROW_NUMBER`

## 문제

상영 시간 기준으로 **3~5번째로 긴** 영화의 순번, 제목, 상영 시간을 구하세요. (`length` 내림차순, 같으면 `title` 순으로 순번)

- 출력: `rn`, `title`, `length` — `rn` 순

**사용 테이블:** `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rn, title, length
FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY length DESC, title) AS rn, title, length
    FROM film
) t
WHERE rn BETWEEN 3 AND 5
ORDER BY rn;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rn | title | length |
|---|---|---|
| 3 | DARN FORRESTER | 185 |
| 4 | GANGS PRIDE | 185 |
| 5 | HOME PITY | 185 |

> 총 3행

</details>

## 해설

**SQLD 빈출**: Oracle 의 `WHERE ROWNUM <= 5 ORDER BY length DESC` 는 **정렬 전에** 5건을 자른 뒤 정렬하므로 틀린 답입니다.
또 `WHERE ROWNUM BETWEEN 3 AND 5` 는 항상 0건입니다 (ROWNUM 은 1부터 순서대로 부여되므로 첫 행이 3이 될 수 없음).
정답은 "정렬한 인라인 뷰 → 바깥에서 번호로 거르기" 이며, MySQL 은 `LIMIT 2, 3` 또는 `ROW_NUMBER()` 를 씁니다.
