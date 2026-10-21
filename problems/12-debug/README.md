# 쿼리 디버깅

잘못된 쿼리 고치기 · 팬아웃 · NULL · 조인 조건

| ID | 제목 | 난이도 | 태그 |
|---|---|---|---|
| [FIX-001](FIX-001.md) | 사라진 고객들 (LEFT JOIN + WHERE) | ★★☆☆☆ 초급 | LEFT JOIN, ON vs WHERE, 디버깅 |
| [FIX-002](FIX-002.md) | 영화가 없는 언어가 1편? (COUNT(*) 함정) | ★★☆☆☆ 초급 | COUNT, LEFT JOIN, 디버깅 |
| [FIX-003](FIX-003.md) | 매출이 두 배로? (조인 팬아웃) | ★★★☆☆ 중급 | 팬아웃, SUM, 집계 후 조인, 디버깅 |
| [FIX-004](FIX-004.md) | 결과가 0행 (NOT IN 과 NULL) | ★★★☆☆ 중급 | NOT IN, NULL, NOT EXISTS, 디버깅 |
| [FIX-005](FIX-005.md) | 마지막 날이 빠진 기간 집계 (BETWEEN) | ★★☆☆☆ 초급 | BETWEEN, DATETIME, 반열린 구간, 디버깅 |
| [FIX-006](FIX-006.md) | 조건이 이상하게 적용됨 (AND/OR 우선순위) | ★★☆☆☆ 초급 | AND, OR, 괄호, 디버깅 |
| [FIX-007](FIX-007.md) | 이전 고객의 값이 섞임 (PARTITION BY 누락) | ★★★☆☆ 중급 | LAG, PARTITION BY, 디버깅 |
| [FIX-008](FIX-008.md) | 마지막 값이 자기 자신 (LAST_VALUE 프레임) | ★★★☆☆ 중급 | LAST_VALUE, 윈도우 프레임, 디버깅 |
| [FIX-009](FIX-009.md) | 윈도우 함수를 WHERE 에 써서 오류 | ★★☆☆☆ 초급 | 윈도우 함수, WHERE, 파생 테이블, 디버깅 |
| [FIX-010](FIX-010.md) | 마지막 대여의 영화 제목 (ONLY_FULL_GROUP_BY) | ★★★☆☆ 중급 | GROUP BY, ONLY_FULL_GROUP_BY, 그룹별 최신 행, 디버깅 |
| [FIX-011](FIX-011.md) | 잘못된 조인 키 | ★★★☆☆ 중급 | 조인 키, 카테시안, 디버깅 |
| [FIX-012](FIX-012.md) | 주소가 통째로 NULL (CONCAT 과 NULL) | ★★☆☆☆ 초급 | CONCAT, CONCAT_WS, NULL, 디버깅 |
| [FIX-013](FIX-013.md) | 비율이 전부 0 (DIV 정수 나눗셈) | ★★☆☆☆ 초급 | DIV, 나눗셈, 형 변환, 디버깅 |
| [FIX-014](FIX-014.md) | 문자열로 정렬된 숫자 | ★★☆☆☆ 초급 | 정렬, 형 변환, CAST, 디버깅 |
| [FIX-015](FIX-015.md) | 동점자가 잘린 TOP 3 | ★★★☆☆ 중급 | LIMIT, RANK, 동점, 디버깅 |
| [FIX-016](FIX-016.md) | 평균의 평균 | ★★★☆☆ 중급 | 평균, 가중 평균, 집계 단위, 디버깅 |
