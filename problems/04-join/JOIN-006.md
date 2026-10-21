# JOIN-006. 재고가 없는 영화

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `LEFT JOIN` `안티 조인` `IS NULL`

## 문제

`film` 에는 등록되어 있지만 **어느 매장에도 재고가 없는** 영화의 `film_id`, `title` 을 `film_id` 순으로 조회하세요.

**사용 테이블:** `film`, `inventory`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.film_id, f.title
FROM film f
LEFT JOIN inventory i ON i.film_id = f.film_id
WHERE i.inventory_id IS NULL
ORDER BY f.film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title |
|---|---|
| 14 | ALICE FANTASIA |
| 33 | APOLLO TEEN |
| 36 | ARGONAUTS TOWN |
| 38 | ARK RIDGEMONT |
| 41 | ARSENIC INDEPENDENCE |
| 87 | BOONDOCK BALLROOM |
| 108 | BUTCH PANTHER |
| 128 | CATCH AMISTAD |
| 144 | CHINATOWN GLADIATOR |
| 148 | CHOCOLATE DUCK |
| 171 | COMMANDMENTS EXPRESS |
| 192 | CROSSING DIVORCE |
| 195 | CROWDS TELEMARK |
| 198 | CRYSTAL BREAKING |
| 217 | DAZED PUNK |
| 221 | DELIVERANCE MULHOLLAND |
| 318 | FIREHOUSE VIETNAM |
| 325 | FLOATS GARDEN |
| 332 | FRANKENSTEIN STRANGER |
| 359 | GLADIATOR WESTWARD |

> 총 42행 중 상위 20행만 표시

</details>

## 해설

- **안티 조인**: "B 에 없는 A". `LEFT JOIN ... WHERE B.pk IS NULL` 또는 `NOT EXISTS` 로 씁니다.
- `IS NULL` 검사는 반드시 **NOT NULL 컬럼(보통 PK)** 에 해야 "매칭 실패"와 "원래 NULL"을 구분할 수 있습니다.
- 결과: 1,000편 중 **42편**은 재고가 없습니다. 반면 재고가 있는 958편은 **모두 한 번 이상 대여**되었습니다.
  DVD 단위로 보면 미대여 재고가 딱 1장(`inventory_id = 5`) 있습니다 — "영화 단위"냐 "재고 단위"냐에 따라 답이 달라집니다.
