# CASE-006. UNION 으로 연락처 목록 만들기

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `UNION ALL`

## 문제

고객과 직원을 하나의 연락처 목록으로 합치세요. 이메일이 `@` 앞 기준 `M` 으로 시작하는 사람만 포함합니다.

- 출력: `type`(`고객`/`직원`), `name`(이름 성), `email` — `type`, `name` 순

**사용 테이블:** `customer`, `staff`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT '고객' AS type, CONCAT(first_name, ' ', last_name) AS name, email
FROM customer
WHERE email LIKE 'M%'
UNION ALL
SELECT '직원', CONCAT(first_name, ' ', last_name), email
FROM staff
WHERE email LIKE 'M%'
ORDER BY type, name;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| type | name | email |
|---|---|---|
| 고객 | MABEL HOLLAND | MABEL.HOLLAND@sakilacustomer.org |
| 고객 | MAE FLETCHER | MAE.FLETCHER@sakilacustomer.org |
| 고객 | MANUEL MURRELL | MANUEL.MURRELL@sakilacustomer.org |
| 고객 | MARC OUTLAW | MARC.OUTLAW@sakilacustomer.org |
| 고객 | MARCIA DEAN | MARCIA.DEAN@sakilacustomer.org |
| 고객 | MARCUS HIDALGO | MARCUS.HIDALGO@sakilacustomer.org |
| 고객 | MARGARET MOORE | MARGARET.MOORE@sakilacustomer.org |
| 고객 | MARGIE WADE | MARGIE.WADE@sakilacustomer.org |
| 고객 | MARIA MILLER | MARIA.MILLER@sakilacustomer.org |
| 고객 | MARIAN MENDOZA | MARIAN.MENDOZA@sakilacustomer.org |
| 고객 | MARIE TURNER | MARIE.TURNER@sakilacustomer.org |
| 고객 | MARILYN ROSS | MARILYN.ROSS@sakilacustomer.org |
| 고객 | MARIO CHEATHAM | MARIO.CHEATHAM@sakilacustomer.org |
| 고객 | MARION OCAMPO | MARION.OCAMPO@sakilacustomer.org |
| 고객 | MARION SNYDER | MARION.SNYDER@sakilacustomer.org |
| 고객 | MARJORIE TUCKER | MARJORIE.TUCKER@sakilacustomer.org |
| 고객 | MARK RINEHART | MARK.RINEHART@sakilacustomer.org |
| 고객 | MARLENE WELCH | MARLENE.WELCH@sakilacustomer.org |
| 고객 | MARSHA DOUGLAS | MARSHA.DOUGLAS@sakilacustomer.org |
| 고객 | MARSHALL THORN | MARSHALL.THORN@sakilacustomer.org |

> 총 52행 중 상위 20행만 표시

</details>

## 해설

`UNION` 은 두 결과를 위아래로 붙입니다. 컬럼 **개수와 순서**가 같아야 하고, 컬럼 이름은 **첫 번째 SELECT** 를 따릅니다.
`ORDER BY` 는 마지막에 한 번만 쓰며 합쳐진 전체 결과에 적용됩니다.
