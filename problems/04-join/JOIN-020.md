# JOIN-020. 대여한 직원과 결제받은 직원

**유형:** 조인 · **난이도:** ★★★☆☆ 중급 · **태그:** `다중 조인` `비교`

## 문제

대여를 처리한 직원(`rental.staff_id`)과 그 대여의 결제를 처리한 직원(`payment.staff_id`)이 **다른** 건수를 구하세요.

- 출력: `rental_staff`, `payment_staff`, `cnt` — `rental_staff`, `payment_staff` 순 (모든 조합 표시)

**사용 테이블:** `rental`, `payment`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT r.staff_id AS rental_staff, p.staff_id AS payment_staff, COUNT(*) AS cnt
FROM rental r
JOIN payment p ON p.rental_id = r.rental_id
GROUP BY r.staff_id, p.staff_id
ORDER BY rental_staff, payment_staff;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rental_staff | payment_staff | cnt |
|---|---|---|
| 1 | 1 | 4008 |
| 1 | 2 | 4032 |
| 2 | 1 | 4046 |
| 2 | 2 | 3958 |

> 총 4행

</details>

## 해설

문제는 "다른 건수"지만 **모든 조합**을 보여주면 같은 경우·다른 경우를 한눈에 비교할 수 있습니다.
데이터 검증 쿼리를 짤 때 이렇게 교차표를 먼저 보는 습관이 유용합니다.
