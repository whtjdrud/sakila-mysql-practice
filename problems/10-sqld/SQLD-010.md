# SQLD-010. OUTER JOIN 결과 건수

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `LEFT OUTER JOIN` `ON vs WHERE` `건수`

## 문제

고객과 **2006년 대여**를 LEFT OUTER JOIN 했을 때의 결과 행 수를 두 가지로 구하세요.

- `on_cnt`: 2006년 조건을 **ON 절**에 둔 경우
- `where_cnt`: 2006년 조건을 **WHERE 절**에 둔 경우

**사용 테이블:** `customer`, `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT
  (SELECT COUNT(*) FROM customer c
     LEFT JOIN rental r ON r.customer_id = c.customer_id AND r.rental_date >= '2006-01-01') AS on_cnt,
  (SELECT COUNT(*) FROM customer c
     LEFT JOIN rental r ON r.customer_id = c.customer_id
    WHERE r.rental_date >= '2006-01-01') AS where_cnt;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| on_cnt | where_cnt |
|---|---|
| 623 | 182 |

> 총 1행

</details>

## 해설

- ON 에 두면: 모든 고객이 보존되고 2006년 대여가 붙습니다 → (2006년 대여 건수) + (2006년 대여가 없는 고객 수)
- WHERE 에 두면: 조인 후 거르므로 NULL 행이 사라져 **INNER JOIN 과 같아집니다** → 2006년 대여 건수
Oracle 의 `(+)` 표기에서도 같은 원리로, 조건에 `(+)` 를 빠뜨리면 아우터 조인이 이너 조인으로 바뀝니다.
