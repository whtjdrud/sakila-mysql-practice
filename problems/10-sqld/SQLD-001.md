# SQLD-001. NULL 의 연산 규칙

**유형:** SQLD 유형 · **난이도:** ★☆☆☆☆ 입문 · **태그:** `NULL` `NVL` `산술 연산`

## 문제

테이블 없이 아래 식의 결과를 한 행으로 출력하세요.

| 컬럼 | 식 |
|---|---|
| `plus` | `NULL + 1` |
| `eq` | `NULL = NULL` |
| `is_null` | `NULL IS NULL` |
| `nvl` | NULL 이면 0 (`IFNULL`) |
| `concat_null` | `CONCAT('A', NULL)` |
| `coalesce3` | `COALESCE(NULL, NULL, 'C')` |

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT NULL + 1                 AS plus,
       NULL = NULL              AS eq,
       NULL IS NULL             AS is_null,
       IFNULL(NULL, 0)          AS nvl,
       CONCAT('A', NULL)        AS concat_null,
       COALESCE(NULL, NULL, 'C') AS coalesce3;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| plus | eq | is_null | nvl | concat_null | coalesce3 |
|---|---|---|---|---|---|
| NULL | NULL | 1 | 0 | NULL | C |

> 총 1행

</details>

## 해설

**SQLD 빈출**: NULL 과의 산술 연산·비교 연산은 모두 **NULL** 입니다. `NULL = NULL` 도 TRUE 가 아닙니다.
- Oracle `NVL(a, b)` = MySQL `IFNULL(a, b)`, Oracle `NVL2(a, b, c)` = MySQL `IF(a IS NOT NULL, b, c)`
- ⚠️ Oracle 은 `'A' || NULL` 이 `'A'` (NULL 을 빈 문자열로 취급)이지만, MySQL `CONCAT('A', NULL)` 은 **NULL** 입니다.
- Oracle 은 빈 문자열 `''` 을 NULL 로 취급하지만 MySQL 은 다릅니다.
