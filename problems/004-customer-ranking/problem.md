# 우수 고객 순위 (윈도우 함수)
level: ⭐⭐⭐ 상

고객별 총 결제 금액을 구하고, 전체 순위와 **국가 내 순위**를 함께 출력하세요.
전체 순위 상위 10명만 출력합니다.

- 출력 컬럼: `customer`(이름 성), `country`, `total_paid`, `overall_rank`, `country_rank`
- 순위는 동점 시 같은 순위를 주는 `RANK()` 사용

**사용 테이블:** `payment`, `customer`, `address`, `city`, `country`
