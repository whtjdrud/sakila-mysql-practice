# 002. 가장 많이 대여된 영화 TOP 10

**난이도:** ⭐⭐ 중

## 문제

전체 기간 동안 대여 횟수가 가장 많은 영화 10편을 구하세요.

- 출력 컬럼: `title`, `rating`(등급), `rental_count`(대여 횟수)
- 대여 횟수 내림차순, 같으면 제목 오름차순

**힌트:** 대여(`rental`)는 영화가 아니라 **재고(`inventory`)** 를 가리킵니다.

**사용 테이블:** `rental`, `inventory`, `film`

## 풀이 쿼리

```sql
SELECT f.title,
       f.rating,
       COUNT(r.rental_id) AS rental_count
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
GROUP BY f.film_id, f.title, f.rating
ORDER BY rental_count DESC, f.title
LIMIT 10;
```

## 실행 결과

| title | rating | rental_count |
|---|---|---|
| BUCKET BROTHERHOOD | PG | 34 |
| ROCKETEER MOTHER | PG-13 | 33 |
| FORWARD TEMPLE | NC-17 | 32 |
| GRIT CLOCKWORK | PG | 32 |
| JUGGLER HARDLY | PG-13 | 32 |
| RIDGEMONT SUBMARINE | PG-13 | 32 |
| SCALAWAG DUCK | NC-17 | 32 |
| APACHE DIVINE | NC-17 | 31 |
| GOODFELLAS SALUTE | PG | 31 |
| HOBBIT ALIEN | PG-13 | 31 |

> 총 10행

## 분석

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
