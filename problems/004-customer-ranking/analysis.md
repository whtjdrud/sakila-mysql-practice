### 핵심 개념
- **CTE(`WITH`)** 로 단계를 나눴습니다: ① 고객별 합계 → ② 순위 계산 → ③ 필터링.
- 윈도우 함수 결과는 같은 SELECT 의 `WHERE` 에서 쓸 수 없습니다. 그래서 `ranked` CTE 로 한 번 감싼 뒤 `WHERE overall_rank <= 10` 을 적용했습니다.
- `PARTITION BY country` 는 국가별로 순위를 **다시 1부터** 매깁니다. GROUP BY 와 달리 행이 줄어들지 않는다는 점이 핵심입니다.

### 결과 해석
- 1위는 **KARL SEAL(미국, 221.55)** — 결제 45건입니다.
- **MARION SNYDER 와 RHONDA KENNEDY 가 194.61 로 공동 4위**이고, 다음 순위는 5가 아니라 **6**입니다. 이것이 `RANK()` 의 특징입니다. (`DENSE_RANK()` 면 5, `ROW_NUMBER()` 면 동점이어도 4·5로 갈립니다.)
- 상위 10명 중 9명이 각 국가 내 1위인데, **ANA BRADLEY 만 국가 내 2위**입니다. 같은 미국의 KARL SEAL 이 있기 때문이죠.
- `Runion` 은 오타가 아니라 Sakila 원본 데이터의 표기(Réunion 의 악센트 문자가 빠진 것)입니다.
