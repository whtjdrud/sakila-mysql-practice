# CASE-010. 이탈 위험 고객 분류

**유형:** 조건식·집합 · **난이도:** ★★★☆☆ 중급 · **태그:** `CASE` `파생 테이블` `세그먼트`

## 문제

고객별 마지막 대여일과 대여 횟수로 다음 세그먼트를 만들고 세그먼트별 고객 수와 평균 결제액(소수 2자리)을 구하세요.
기준일은 2005년 마지막 대여 다음 날인 `'2005-08-24'` 이며 2006년 대여는 제외합니다.

| 세그먼트 | 조건 |
|---|---|
| 충성 | 마지막 대여가 기준일 2일 이내 & 대여 30회 이상 |
| 활동 | 마지막 대여가 기준일 2일 이내 |
| 이탈위험 | 그 외 |

- 출력: `segment`, `customers`, `avg_paid` — 충성 → 활동 → 이탈위험 순

**사용 테이블:** `rental`, `payment`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT segment, COUNT(*) AS customers, ROUND(AVG(paid), 2) AS avg_paid
FROM (
    SELECT r.customer_id,
           CASE WHEN MAX(r.rental_date) >= '2005-08-24' - INTERVAL 2 DAY AND COUNT(*) >= 30 THEN '충성'
                WHEN MAX(r.rental_date) >= '2005-08-24' - INTERVAL 2 DAY THEN '활동'
                ELSE '이탈위험' END AS segment,
           (SELECT SUM(p.amount) FROM payment p
             WHERE p.customer_id = r.customer_id AND p.payment_date < '2006-01-01') AS paid
    FROM rental r
    WHERE r.rental_date < '2006-01-01'
    GROUP BY r.customer_id
) t
GROUP BY segment
ORDER BY FIELD(segment, '충성', '활동', '이탈위험');
```

</details>

<details>
<summary>실행 결과 보기</summary>

| segment | customers | avg_paid |
|---|---|---|
| 충성 | 144 | 139.46 |
| 활동 | 383 | 102.55 |
| 이탈위험 | 72 | 104.75 |

> 총 3행

</details>

## 해설

CASE 안에서 집계 함수(`MAX`, `COUNT`)를 쓸 수 있습니다. **RFM 분석**(Recency·Frequency·Monetary)의 간단한 버전입니다.
조건의 순서가 중요합니다 — `충성` 을 `활동` 보다 먼저 검사해야 합니다.
기준일과 기간 설정이 지표를 좌우합니다. 기준일을 `'2005-09-01'` 로 잡으면 마지막 대여(08-23)가 7일 밖이라 **전원이 이탈위험**,
`'2005-08-24'` 기준 7일이면 **전원이 활동**이 됩니다. 8월 하순 대여가 몰려 있어 2일 창(window)에서야 세 세그먼트가 고르게 나뉩니다.
