# CASE-003. 임의 순서로 정렬하기

**유형:** 조건식·집합 · **난이도:** ★★☆☆☆ 초급 · **태그:** `ORDER BY CASE`

## 문제

장르 `Action`, `Comedy`, `Drama` 를 **이 순서대로 맨 위에**, 나머지 장르는 그 아래에 이름 순으로 정렬해 모든 장르의 `name` 을 조회하세요.

**사용 테이블:** `category`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT name
FROM category
ORDER BY CASE name
           WHEN 'Action' THEN 1
           WHEN 'Comedy' THEN 2
           WHEN 'Drama'  THEN 3
           ELSE 4
         END,
         name;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| name |
|---|
| Action |
| Comedy |
| Drama |
| Animation |
| Children |
| Classics |
| Documentary |
| Family |
| Foreign |
| Games |
| Horror |
| Music |
| New |
| Sci-Fi |
| Sports |
| Travel |

> 총 16행

</details>

## 해설

`ORDER BY` 에도 CASE 를 쓸 수 있습니다. "추천 항목 먼저" 같은 비즈니스 정렬에 유용합니다.
MySQL 전용 `FIELD()` 를 쓸 때는 목록에 없는 값이 0이 되어 **맨 앞**으로 오니 주의하세요.
