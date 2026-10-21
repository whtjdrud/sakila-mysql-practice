# SQLD-004. DECODE 를 CASE 로

**유형:** SQLD 유형 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `DECODE` `CASE`

## 문제

Oracle 의 아래 쿼리와 같은 결과를 MySQL 로 작성하세요.

```sql
SELECT store_id,
       SUM(DECODE(active, 1, 1, 0)) AS active_cnt,
       SUM(DECODE(active, 0, 1, 0)) AS dormant_cnt
FROM customer
GROUP BY store_id
ORDER BY store_id;
```

**사용 테이블:** `customer`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT store_id,
       SUM(CASE active WHEN 1 THEN 1 ELSE 0 END) AS active_cnt,
       SUM(CASE active WHEN 0 THEN 1 ELSE 0 END) AS dormant_cnt
FROM customer
GROUP BY store_id
ORDER BY store_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| store_id | active_cnt | dormant_cnt |
|---|---|---|
| 1 | 318 | 8 |
| 2 | 266 | 7 |

> 총 2행

</details>

## 해설

`DECODE(expr, 값1, 결과1, 값2, 결과2, ..., 기본값)` 은 Oracle 전용이며 **단순 CASE** 와 같습니다.
단, DECODE 는 `NULL` 끼리 같다고 보지만 `CASE expr WHEN NULL` 은 절대 참이 되지 않는다는 차이가 있습니다(시험 단골).
