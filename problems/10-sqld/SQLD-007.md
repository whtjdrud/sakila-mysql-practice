# SQLD-007. NULL 의 정렬 위치 (Oracle vs MySQL)

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `ORDER BY` `NULL 정렬` `NULLS LAST`

## 문제

고객 1~3번의 대여 중 2005-08-20 이후 대여의 `rental_id`, `customer_id`, `return_date` 를
**반납일 오름차순**으로 정렬하되, Oracle 의 기본 동작처럼 **NULL 이 맨 뒤**에 오게 하세요. 같으면 `rental_id` 순.

**사용 테이블:** `rental`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT rental_id, customer_id, return_date
FROM rental
WHERE customer_id <= 3 AND rental_date >= '2005-08-20'
ORDER BY return_date IS NULL, return_date, rental_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| rental_id | customer_id | return_date |
|---|---|---|
| 14762 | 1 | 2005-08-23 01:30:57 |
| 15038 | 3 | 2005-08-23 14:39:27 |
| 15907 | 2 | 2005-08-25 23:23:35 |
| 13610 | 3 | 2005-08-26 00:44:12 |
| 15619 | 3 | 2005-08-26 07:21:14 |
| 14825 | 1 | 2005-08-27 07:01:57 |
| 14475 | 2 | 2005-08-27 08:59:32 |
| 15298 | 1 | 2005-08-28 22:49:37 |
| 14743 | 2 | 2005-08-29 00:18:56 |
| 14699 | 3 | 2005-08-29 18:08:48 |
| 15315 | 1 | 2005-08-30 01:51:46 |
| 15145 | 2 | 2005-08-31 15:51:04 |

> 총 12행

</details>

## 해설

**SQLD 빈출**: Oracle 은 NULL 을 **가장 큰 값**으로 취급해 ASC 에서 맨 뒤, DESC 에서 맨 앞에 둡니다.
MySQL·SQL Server 는 반대로 **가장 작은 값**으로 취급합니다. Oracle 은 `NULLS FIRST / NULLS LAST` 로 바꿀 수 있지만 MySQL 은 `IS NULL` 정렬 키를 씁니다.
