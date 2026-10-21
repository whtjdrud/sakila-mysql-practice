# SQLD-006. GROUP BY 없는 HAVING

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `HAVING` `전체 그룹`

## 문제

전체 결제의 평균 금액이 **4 이상일 때만** 평균 금액(소수 2자리)과 결제 건수를 출력하세요. GROUP BY 를 쓰지 마세요.

- 출력: `avg_amount`, `payments`

**사용 테이블:** `payment`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT ROUND(AVG(amount), 2) AS avg_amount, COUNT(*) AS payments
FROM payment
HAVING AVG(amount) >= 4;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| avg_amount | payments |
|---|---|
| 4.20 | 16049 |

> 총 1행

</details>

## 해설

**SQLD 빈출**: GROUP BY 없이 HAVING 을 쓰면 **테이블 전체가 하나의 그룹**이 됩니다. 조건이 거짓이면 0행, 참이면 1행이 나옵니다.
(WHERE 로 집계 조건을 걸 수 없다는 것과 함께 자주 출제됩니다.) 조건을 `>= 5` 로 바꿔 0행이 되는지 확인해 보세요.
