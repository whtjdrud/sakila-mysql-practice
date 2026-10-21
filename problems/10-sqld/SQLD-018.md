# SQLD-018. RATIO_TO_REPORT

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `RATIO_TO_REPORT` `SUM OVER` `비율`

## 문제

고객 1번의 결제마다 **고객 전체 결제액 대비 비율**을 구하세요. (Oracle 의 `RATIO_TO_REPORT(amount) OVER ()`)

- 출력: `payment_id`, `amount`, `ratio`(소수 4자리) — `payment_id` 순

**사용 테이블:** `payment`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT payment_id, amount,
       ROUND(amount / SUM(amount) OVER (), 4) AS ratio
FROM payment
WHERE customer_id = 1
ORDER BY payment_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| payment_id | amount | ratio |
|---|---|---|
| 1 | 2.99 | 0.0252 |
| 2 | 0.99 | 0.0083 |
| 3 | 5.99 | 0.0505 |
| 4 | 0.99 | 0.0083 |
| 5 | 9.99 | 0.0842 |
| 6 | 4.99 | 0.0420 |
| 7 | 4.99 | 0.0420 |
| 8 | 0.99 | 0.0083 |
| 9 | 3.99 | 0.0336 |
| 10 | 5.99 | 0.0505 |
| 11 | 5.99 | 0.0505 |
| 12 | 4.99 | 0.0420 |
| 13 | 4.99 | 0.0420 |
| 14 | 7.99 | 0.0673 |
| 15 | 2.99 | 0.0252 |
| 16 | 4.99 | 0.0420 |
| 17 | 4.99 | 0.0420 |
| 18 | 0.99 | 0.0083 |
| 19 | 0.99 | 0.0083 |
| 20 | 2.99 | 0.0252 |

> 총 32행 중 상위 20행만 표시

</details>

## 해설

`RATIO_TO_REPORT(x) OVER (PARTITION BY ...)` = `x / SUM(x) OVER (PARTITION BY ...)`. 결과의 합은 항상 1 입니다.
SQLD 의 **비율 함수** 네 가지: `RATIO_TO_REPORT`, `PERCENT_RANK`, `CUME_DIST`, `NTILE` — 정의를 구분해 두세요 (WIN-015, WIN-016 참고).
