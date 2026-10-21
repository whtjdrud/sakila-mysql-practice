# SQLD-009. NATURAL JOIN 의 함정

**유형:** SQLD 유형 · **난이도:** ★★★☆☆ 중급 · **태그:** `NATURAL JOIN` `USING`

## 문제

`film_category` 와 `category` 를 조인한 결과 행 수를 두 가지 방법으로 구해 비교하세요.

- `using_cnt`: `USING (category_id)` 로 조인한 행 수
- `natural_cnt`: `NATURAL JOIN` 으로 조인한 행 수

**사용 테이블:** `film_category`, `category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT (SELECT COUNT(*) FROM film_category JOIN category USING (category_id)) AS using_cnt,
       (SELECT COUNT(*) FROM film_category NATURAL JOIN category)            AS natural_cnt;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| using_cnt | natural_cnt |
|---|---|
| 1000 | 0 |

> 총 1행

</details>

## 해설

결과: `1000` vs `0`. NATURAL JOIN 은 **이름이 같은 모든 컬럼**으로 조인하는데, 두 테이블 모두 `last_update` 를 가지고 있어
`category_id` 뿐 아니라 `last_update` 까지 같아야 하는 조건이 붙기 때문입니다.
**SQLD 빈출**: NATURAL JOIN·USING 에 쓰인 컬럼에는 **테이블 별칭(접두사)을 붙일 수 없다**는 것도 자주 나옵니다.
