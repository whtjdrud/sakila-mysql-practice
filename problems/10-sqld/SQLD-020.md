# SQLD-020. LAG 의 오프셋과 기본값

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `LAG` `LEAD` `기본값`

## 문제

고객 1번의 결제를 결제일 순으로 나열하고, **2건 전** 결제 금액(없으면 0)과 **다음** 결제 금액(없으면 NULL)을 구하세요.

- 출력: `payment_id`, `amount`, `amount_2_before`, `next_amount` — `payment_date`, `payment_id` 순

**사용 테이블:** `payment`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT payment_id, amount,
       LAG(amount, 2, 0) OVER w AS amount_2_before,
       LEAD(amount)      OVER w AS next_amount
FROM payment
WHERE customer_id = 1
WINDOW w AS (ORDER BY payment_date, payment_id)
ORDER BY payment_date, payment_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| payment_id | amount | amount_2_before | next_amount |
|---|---|---|---|
| 1 | 2.99 | 0.00 | 0.99 |
| 2 | 0.99 | 0.00 | 5.99 |
| 3 | 5.99 | 2.99 | 0.99 |
| 4 | 0.99 | 0.99 | 9.99 |
| 5 | 9.99 | 5.99 | 4.99 |
| 6 | 4.99 | 0.99 | 4.99 |
| 7 | 4.99 | 9.99 | 0.99 |
| 8 | 0.99 | 4.99 | 3.99 |
| 9 | 3.99 | 4.99 | 5.99 |
| 10 | 5.99 | 0.99 | 5.99 |
| 11 | 5.99 | 3.99 | 4.99 |
| 12 | 4.99 | 5.99 | 4.99 |
| 13 | 4.99 | 5.99 | 7.99 |
| 14 | 7.99 | 4.99 | 2.99 |
| 15 | 2.99 | 4.99 | 4.99 |
| 16 | 4.99 | 7.99 | 4.99 |
| 17 | 4.99 | 2.99 | 0.99 |
| 18 | 0.99 | 4.99 | 0.99 |
| 19 | 0.99 | 4.99 | 2.99 |
| 20 | 2.99 | 0.99 | 2.99 |

> 총 32행 중 상위 20행만 표시

</details>

## 해설

`LAG(컬럼, 오프셋, 기본값)` — 오프셋 기본은 1, 기본값을 생략하면 NULL. 처음 두 행은 2건 전이 없어 0 이 됩니다.
Oracle 은 `LAG(x, 2, 0) IGNORE NULLS` 처럼 NULL 건너뛰기 옵션도 있지만 MySQL 은 지원하지 않습니다.
