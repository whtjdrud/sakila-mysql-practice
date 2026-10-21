# 장르별 매출 1위 배우
level: ⭐⭐⭐⭐ 최상

각 장르에서, 출연 영화들이 벌어들인 **매출 합계가 가장 큰 배우**를 구하세요.

- 출력 컬럼: `category`, `actor`(이름 성), `revenue`
- 동점이면 모두 출력 (`RANK()` 사용)
- 장르명 오름차순

**힌트:** 결제 → 대여 → 재고 → 영화 → (장르, 배우) 로 이어지는 6단 조인입니다.
영화 한 편의 매출은 출연 배우 모두에게 각각 집계됩니다.

**사용 테이블:** `payment`, `rental`, `inventory`, `film_category`, `category`, `film_actor`, `actor`
