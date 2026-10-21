### 핵심 개념
- Sakila 의 대여 구조: `rental → inventory → film`. 대여 기록은 **DVD 실물(재고) 1장**을 가리키므로, 영화 단위로 집계하려면 반드시 `inventory` 를 거쳐야 합니다.
- `COUNT(r.rental_id)` 는 NULL 이 아닌 대여 건만 세므로 의도가 명확합니다.

### 결과 해석
- 1위는 **BUCKET BROTHERHOOD(34회)**, 2위 ROCKETEER MOTHER(33회)입니다.
- 등급을 보면 TOP 10 이 PG, PG-13, NC-17 에 몰려 있고 G·R 등급은 없습니다.

### ⚠️ 함정: `LIMIT` 은 동점을 자릅니다
결과의 8~10위는 모두 31회인데, 실제로 **31회 이상 대여된 영화는 16편**입니다.
즉 31회인 영화 중 일부는 제목 알파벳 순서 때문에 TOP 10 에서 잘려 나갔습니다.
"상위 10위까지의 영화"를 공정하게 뽑으려면 윈도우 함수를 사용하세요.

```sql
SELECT * FROM (
  SELECT f.title, COUNT(*) AS rental_count,
         RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
  FROM rental r
  JOIN inventory i USING (inventory_id)
  JOIN film f USING (film_id)
  GROUP BY f.film_id, f.title
) t
WHERE rnk <= 10;
```
