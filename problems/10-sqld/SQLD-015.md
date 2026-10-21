# SQLD-015. MINUS 를 EXCEPT 로

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `MINUS` `EXCEPT` `집합 연산`

## 문제

배우의 성(`last_name`) 중 **고객의 성으로는 쓰이지 않는** 성을 중복 없이 구하세요. (Oracle 의 `MINUS`)

- 출력: `last_name` — `last_name` 순

**사용 테이블:** `actor`, `customer`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT last_name FROM actor
EXCEPT
SELECT last_name FROM customer
ORDER BY last_name;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| last_name |
|---|
| AKROYD |
| ASTAIRE |
| BACALL |
| BALE |
| BALL |
| BARRYMORE |
| BASINGER |
| BENING |
| BERGEN |
| BERGMAN |
| BIRCH |
| BLOOM |
| BOLGER |
| BRIDGES |
| BRODY |
| BULLOCK |
| CAGE |
| CARREY |
| CHAPLIN |
| CHASE |

> 총 99행 중 상위 20행만 표시

</details>

## 해설

Oracle 은 `MINUS`, 표준·SQL Server·MySQL(8.0.31+) 은 `EXCEPT` 입니다. 결과는 **중복이 제거**됩니다.
**SQLD 빈출**: 집합 연산의 결과 컬럼 이름은 **첫 번째 SELECT** 를 따르고, ORDER BY 는 **마지막에 한 번만** 씁니다.
