# 윈도우 함수

순위 · 누적 · 이동 평균 · LAG/LEAD

| ID | 제목 | 난이도 | 태그 |
|---|---|---|---|
| [WIN-001](WIN-001.md) | 행 번호 붙이기 | ★★☆☆☆ 초급 | ROW_NUMBER, OVER |
| [WIN-002](WIN-002.md) | ROW_NUMBER · RANK · DENSE_RANK 비교 | ★★☆☆☆ 초급 | RANK, DENSE_RANK, ROW_NUMBER |
| [WIN-003](WIN-003.md) | 장르별 영화 순위 | ★★☆☆☆ 초급 | PARTITION BY, ROW_NUMBER |
| [WIN-004](WIN-004.md) | 공정한 TOP 10 (동점 포함) | ★★★☆☆ 중급 | RANK, 동점 처리 |
| [WIN-005](WIN-005.md) | 전체 대비 비율 | ★★☆☆☆ 초급 | SUM OVER, 비율 |
| [WIN-006](WIN-006.md) | 그룹 평균과 비교 | ★★☆☆☆ 초급 | AVG OVER, PARTITION BY |
| [WIN-007](WIN-007.md) | 일별 누적 매출 | ★★☆☆☆ 초급 | 누적합, SUM OVER ORDER BY |
| [WIN-008](WIN-008.md) | 고객별 누적 결제와 결제 순번 | ★★★☆☆ 중급 | 누적합, PARTITION BY, ROWS |
| [WIN-009](WIN-009.md) | 7일 이동 평균 | ★★★☆☆ 중급 | 이동 평균, ROWS BETWEEN |
| [WIN-010](WIN-010.md) | 직전 대여와의 간격 (LAG) | ★★☆☆☆ 초급 | LAG, 이전 행 |
| [WIN-011](WIN-011.md) | 전월 대비 매출 증감률 | ★★★☆☆ 중급 | LAG, 증감률 |
| [WIN-012](WIN-012.md) | 다음 대여까지 걸린 시간 (LEAD) | ★★★☆☆ 중급 | LEAD, 재방문 간격 |
| [WIN-013](WIN-013.md) | 첫 값과 마지막 값 | ★★★☆☆ 중급 | FIRST_VALUE, LAST_VALUE, 프레임 |
| [WIN-014](WIN-014.md) | N번째 값 | ★★★☆☆ 중급 | NTH_VALUE |
| [WIN-015](WIN-015.md) | 4분위 그룹 나누기 | ★★★☆☆ 중급 | NTILE, 분위수 |
| [WIN-016](WIN-016.md) | 백분위 순위 | ★★★☆☆ 중급 | PERCENT_RANK, CUME_DIST |
| [WIN-017](WIN-017.md) | 중앙값 (윈도우 함수) | ★★★★☆ 고급 | 중앙값, ROW_NUMBER, COUNT OVER |
| [WIN-018](WIN-018.md) | 매장별 매출 점유율 추이 | ★★★☆☆ 중급 | PARTITION BY, 점유율 |
| [WIN-019](WIN-019.md) | 처음으로 누적 50% 를 넘는 장르 (파레토) | ★★★★☆ 고급 | 누적 비율, 파레토 |
| [WIN-020](WIN-020.md) | 연속 증가 구간 찾기 | ★★★★☆ 고급 | LAG, 플래그, 누적합 그룹 |
| [WIN-021](WIN-021.md) | 고객의 N번째 대여 장르 | ★★★☆☆ 중급 | ROW_NUMBER, 첫 구매 분석 |
| [WIN-022](WIN-022.md) | 매장별 일 매출 순위 변동 | ★★★★☆ 고급 | RANK, LAG, 순위 변동 |
| [WIN-023](WIN-023.md) | 이전 최고 기록 갱신 | ★★★★☆ 고급 | MAX OVER, 신기록 |
| [WIN-024](WIN-024.md) | 배우 출연작의 개봉 순서별 등급 | ★★☆☆☆ 초급 | ROW_NUMBER, PARTITION BY, 다중 정렬 |
| [WIN-025](WIN-025.md) | 결제 금액 이상치 탐지 | ★★★★☆ 고급 | AVG OVER, STDDEV OVER, Z-점수 |
| [WIN-026](WIN-026.md) | 대여 간격 분포 (LAG + 구간화) | ★★★☆☆ 중급 | LAG, 구간화, 분포 |
