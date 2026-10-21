# CASE-018. 월별 신규·유지·이탈 고객

**유형:** 조건식·집합 · **난이도:** ★★★★★ 최고급 · **태그:** `UNION ALL` `EXISTS` `고객 흐름`

## 문제

2005-06 ~ 2005-08 각 달에 대해 고객 흐름을 구하세요.

- `신규`: 이번 달 대여했고, 이전 달까지 대여 기록이 없음
- `유지`: 이번 달과 직전 달 모두 대여
- `복귀`: 이번 달 대여, 직전 달은 없지만 그 이전에는 있음
- `이탈`: 직전 달 대여했지만 이번 달은 없음

출력: `month`(YYYY-MM-01), `flow`, `customers` — `month`, 신규 → 유지 → 복귀 → 이탈 순

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT month, flow, COUNT(*) AS customers
FROM (
    SELECT m.month, a.customer_id,
           CASE WHEN NOT EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = a.customer_id AND r.rental_date < m.month)
                     THEN '신규'
                WHEN EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = a.customer_id
                               AND r.rental_date >= m.month - INTERVAL 1 MONTH AND r.rental_date < m.month)
                     THEN '유지'
                ELSE '복귀' END AS flow
    FROM (SELECT DATE('2005-06-01') AS month UNION ALL SELECT '2005-07-01' UNION ALL SELECT '2005-08-01') m
    JOIN (SELECT DISTINCT customer_id, DATE_FORMAT(rental_date, '%Y-%m-01') AS month FROM rental) a
      ON a.month = m.month
    UNION ALL
    SELECT m.month, p.customer_id, '이탈'
    FROM (SELECT DATE('2005-06-01') AS month UNION ALL SELECT '2005-07-01' UNION ALL SELECT '2005-08-01') m
    JOIN (SELECT DISTINCT customer_id, DATE_FORMAT(rental_date, '%Y-%m-01') AS month FROM rental) p
      ON p.month = m.month - INTERVAL 1 MONTH
    WHERE NOT EXISTS (SELECT 1 FROM rental r WHERE r.customer_id = p.customer_id
                        AND r.rental_date >= m.month AND r.rental_date < m.month + INTERVAL 1 MONTH)
) t
GROUP BY month, flow
ORDER BY month, FIELD(flow, '신규', '유지', '복귀', '이탈');
```

</details>

<details>
<summary>실행 결과 보기</summary>

| month | flow | customers |
|---|---|---|
| 2005-06-01 | 신규 | 78 |
| 2005-06-01 | 유지 | 512 |
| 2005-06-01 | 이탈 | 8 |
| 2005-07-01 | 신규 | 1 |
| 2005-07-01 | 유지 | 590 |
| 2005-07-01 | 복귀 | 8 |
| 2005-08-01 | 유지 | 599 |

> 총 7행

</details>

## 해설

이번 달 활동 고객(신규/유지/복귀)과 지난달 활동했지만 이번 달 없는 고객(이탈)은 **출발 집합이 달라서** 하나의 CASE 로 표현할 수 없습니다.
그래서 두 결과를 `UNION ALL` 로 합쳤습니다. 검산: (지난달 활동 고객) = 유지 + 이탈 이 되어야 합니다.
