# JOIN-007. 영화가 없는 장르까지 포함

**유형:** 조인 · **난이도:** ★★☆☆☆ 초급 · **태그:** `LEFT JOIN` `COUNT 함정`

## 문제

모든 언어(`language`)별 영화 수를 구하세요. 영화가 없는 언어도 **0** 으로 표시되어야 합니다.

- 출력: `language`, `films` — `films` 내림차순, `language` 순

**사용 테이블:** `language`, `film`

<details>
<summary>정답 쿼리 보기</summary>

```sql
SELECT l.name AS language, COUNT(f.film_id) AS films
FROM language l
LEFT JOIN film f ON f.language_id = l.language_id
GROUP BY l.language_id, l.name
ORDER BY films DESC, language;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| language | films |
|---|---|
| English | 1000 |
| French | 0 |
| German | 0 |
| Italian | 0 |
| Japanese | 0 |
| Mandarin | 0 |

> 총 6행

</details>

## 해설

LEFT JOIN 후 `COUNT(*)` 를 쓰면 매칭이 없는 언어도 **1** 로 셉니다 (NULL 로 채워진 행이 1개 있으므로).
반드시 오른쪽 테이블의 컬럼으로 `COUNT(f.film_id)` 를 해야 0이 나옵니다. Sakila 의 영화는 모두 English 입니다.
