# SQLD-025. 정규 표현식 함수

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `REGEXP_SUBSTR` `REGEXP_REPLACE` `정규식`

## 문제

주소(`address`)의 맨 앞 번지수를 `REGEXP_SUBSTR` 로 뽑아 `house_no` 로, 번지수와 공백을 제거한 도로명을 `REGEXP_REPLACE` 로 만들어 `street` 로 출력하세요.
`address_id` 1~10번, `address_id` 순.

- 출력: `address_id`, `address`, `house_no`, `street`

**사용 테이블:** `address`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT address_id, address,
       REGEXP_SUBSTR(address, '^[0-9]+') AS house_no,
       REGEXP_REPLACE(address, '^[0-9]+ +', '') AS street
FROM address
WHERE address_id <= 10
ORDER BY address_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| address_id | address | house_no | street |
|---|---|---|---|
| 1 | 47 MySakila Drive | 47 | MySakila Drive |
| 2 | 28 MySQL Boulevard | 28 | MySQL Boulevard |
| 3 | 23 Workhaven Lane | 23 | Workhaven Lane |
| 4 | 1411 Lillydale Drive | 1411 | Lillydale Drive |
| 5 | 1913 Hanoi Way | 1913 | Hanoi Way |
| 6 | 1121 Loja Avenue | 1121 | Loja Avenue |
| 7 | 692 Joliet Street | 692 | Joliet Street |
| 8 | 1566 Inegl Manor | 1566 | Inegl Manor |
| 9 | 53 Idfu Parkway | 53 | Idfu Parkway |
| 10 | 1795 Santiago de Compostela Way | 1795 | Santiago de Compostela Way |

> 총 10행

</details>

## 해설

`REGEXP_SUBSTR`, `REGEXP_REPLACE`, `REGEXP_INSTR`, `REGEXP_LIKE` 는 Oracle 과 MySQL 8.0 모두 지원하며 SQLD 출제 범위에 들어갔습니다.
`^` 시작, `[0-9]+` 숫자 1개 이상, ` +` 공백 1개 이상. 번지수가 없는 주소에서는 `house_no` 가 NULL 이 됩니다.
