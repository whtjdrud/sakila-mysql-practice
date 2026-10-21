# SQLD-005. NVL2 를 IF 로

**유형:** SQLD 유형 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `NVL2` `IF`

## 문제

Oracle 의 `NVL2(return_date, '반납', '미반납')` 과 같은 의미로, 직원(`rental.staff_id`)별 반납/미반납 건수를 구하세요.

- 출력: `staff_id`, `status`, `rentals` — `staff_id`, `status` 순

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT staff_id,
       IF(return_date IS NOT NULL, '반납', '미반납') AS status,
       COUNT(*) AS rentals
FROM rental
GROUP BY staff_id, status
ORDER BY staff_id, status;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| staff_id | status | rentals |
|---|---|---|
| 1 | 미반납 | 85 |
| 1 | 반납 | 7955 |
| 2 | 미반납 | 98 |
| 2 | 반납 | 7906 |

> 총 4행

</details>

## 해설

`NVL2(a, b, c)`: a 가 NULL 이 **아니면** b, NULL 이면 c. 인자 순서를 헷갈리기 쉬운 시험 단골입니다.
MySQL 에는 NVL2 가 없으므로 `IF(a IS NOT NULL, b, c)` 또는 `CASE WHEN a IS NOT NULL THEN b ELSE c END` 를 씁니다.
