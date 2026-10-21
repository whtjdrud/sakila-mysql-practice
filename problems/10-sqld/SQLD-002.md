# SQLD-002. 집계 함수는 NULL 을 무시한다

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `AVG` `COUNT` `NULL`

## 문제

대여 기간(일, `DATEDIFF(return_date, rental_date)`)에 대해 다음을 한 행으로 구하세요. 미반납은 return_date 가 NULL 입니다.

- `cnt_all`: `COUNT(*)`
- `cnt_days`: 대여 기간의 `COUNT`
- `avg_ignore_null`: 대여 기간의 평균 (소수 4자리)
- `avg_null_as_zero`: 미반납을 0일로 보고 낸 평균 (소수 4자리)
- `sum_div_all`: 대여 기간 합계 / `COUNT(*)` (소수 4자리)

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT COUNT(*) AS cnt_all,
       COUNT(DATEDIFF(return_date, rental_date)) AS cnt_days,
       ROUND(AVG(DATEDIFF(return_date, rental_date)), 4) AS avg_ignore_null,
       ROUND(AVG(IFNULL(DATEDIFF(return_date, rental_date), 0)), 4) AS avg_null_as_zero,
       ROUND(SUM(DATEDIFF(return_date, rental_date)) / COUNT(*), 4) AS sum_div_all
FROM rental;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| cnt_all | cnt_days | avg_ignore_null | avg_null_as_zero | sum_div_all |
|---|---|---|---|---|
| 16044 | 15861 | 5.0252 | 4.9679 | 4.9679 |

> 총 1행

</details>

## 해설

**SQLD 빈출**: `AVG(col)` = `SUM(col) / COUNT(col)` 이지 `SUM(col) / COUNT(*)` 가 아닙니다. NULL 행은 분모에서도 빠집니다.
그래서 `avg_null_as_zero` 와 `sum_div_all` 이 같고, `avg_ignore_null` 만 다릅니다.
`COUNT(*)` 는 NULL 을 포함한 행 수, `COUNT(col)` 은 NULL 이 아닌 값의 수입니다.
