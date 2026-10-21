# 카탈로그엔 있지만 재고가 없는 영화
level: ⭐⭐⭐ 상

`film` 테이블에는 등록되어 있지만 **어느 매장에도 재고(inventory)가 없는** 영화를 찾으세요.
장르도 함께 출력합니다.

- 출력 컬럼: `film_id`, `title`, `category`
- `film_id` 오름차순

**생각해볼 점:** `LEFT JOIN ... IS NULL` 과 `NOT EXISTS` 중 무엇을 쓸까요?
그리고 "재고는 있지만 한 번도 대여되지 않은 영화"는 몇 편일까요?

**사용 테이블:** `film`, `inventory`, `film_category`, `category`
