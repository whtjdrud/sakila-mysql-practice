# CASE-014. 집합 연산 조합

**유형:** 조건식·집합 · **난이도:** ★★★★☆ 고급 · **태그:** `UNION` `EXCEPT` `INTERSECT` `우선순위`

## 문제

다음 세 집합으로 결과를 구하세요 (모두 `film_id` 집합).

- A: `Action` 장르 영화
- B: `PENELOPE GUINESS` 출연작
- C: 2번 매장에 재고가 있는 영화

**(A ∪ B) − C** 에 속하는 영화의 `film_id`, `title` 을 `film_id` 순으로 조회하세요.

**사용 테이블:** `film`, `film_category`, `category`, `film_actor`, `actor`, `inventory`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT f.film_id, f.title
FROM film f
WHERE f.film_id IN (
    (SELECT fc.film_id FROM film_category fc JOIN category c ON c.category_id = fc.category_id
      WHERE c.name = 'Action'
     UNION
     SELECT fa.film_id FROM film_actor fa JOIN actor a ON a.actor_id = fa.actor_id
      WHERE a.first_name = 'PENELOPE' AND a.last_name = 'GUINESS')
    EXCEPT
    SELECT i.film_id FROM inventory i WHERE i.store_id = 2
)
ORDER BY f.film_id;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| film_id | title |
|---|---|
| 29 | ANTITRUST TOMATOES |
| 38 | ARK RIDGEMONT |
| 106 | BULWORTH COMMANDMENTS |
| 205 | DANCES NONE |
| 277 | ELEPHANT TROJAN |
| 318 | FIREHOUSE VIETNAM |
| 360 | GLASS DYING |
| 371 | GOSFORD DONNIE |
| 375 | GRAIL FRANKENSTEIN |
| 499 | KING EVOLUTION |
| 530 | LORD ARIZONA |
| 594 | MONTEZUMA COMMAND |
| 732 | RINGS HEARTBREAKERS |
| 793 | SHRUNK DIVINE |
| 802 | SKY MIRACLE |
| 825 | SPEAKEASY DATE |
| 832 | SPLASH GUMP |
| 927 | UPRISING UPTOWN |
| 968 | WEREWOLF LOLA |

> 총 19행

</details>

## 해설

표준 SQL 에서 `INTERSECT` 는 `UNION`/`EXCEPT` 보다 우선순위가 높고, `UNION` 과 `EXCEPT` 는 왼쪽부터 계산됩니다.
의도를 분명히 하려면 **괄호**로 묶으세요. 집합 연산 결과를 `IN (...)` 안에 넣어 원래 테이블과 조인할 수 있습니다.
