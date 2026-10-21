# SQLD 유형

SQLD 빈출 개념 · Oracle 문법과의 차이 · EMP 계층 질의

| ID | 제목 | 난이도 | 태그 |
|---|---|---|---|
| [SQLD-001](SQLD-001.md) | NULL 의 연산 규칙 | ★☆☆☆☆ 입문 | NULL, NVL, 산술 연산 |
| [SQLD-002](SQLD-002.md) | 집계 함수는 NULL 을 무시한다 | ★★☆☆☆ 초급 | AVG, COUNT, NULL |
| [SQLD-003](SQLD-003.md) | ORDER BY 위치 번호와 별칭 | ★☆☆☆☆ 입문 | ORDER BY, 위치 번호, 별칭 |
| [SQLD-004](SQLD-004.md) | DECODE 를 CASE 로 | ★☆☆☆☆ 입문 | DECODE, CASE |
| [SQLD-005](SQLD-005.md) | NVL2 를 IF 로 | ★☆☆☆☆ 입문 | NVL2, IF |
| [SQLD-006](SQLD-006.md) | GROUP BY 없는 HAVING | ★★☆☆☆ 초급 | HAVING, 전체 그룹 |
| [SQLD-007](SQLD-007.md) | NULL 의 정렬 위치 (Oracle vs MySQL) | ★★☆☆☆ 초급 | ORDER BY, NULL 정렬, NULLS LAST |
| [SQLD-008](SQLD-008.md) | ROWNUM 과 Top-N 의 함정 | ★★☆☆☆ 초급 | ROWNUM, Top-N, ROW_NUMBER |
| [SQLD-009](SQLD-009.md) | NATURAL JOIN 의 함정 | ★★★☆☆ 중급 | NATURAL JOIN, USING |
| [SQLD-010](SQLD-010.md) | OUTER JOIN 결과 건수 | ★★★☆☆ 중급 | LEFT OUTER JOIN, ON vs WHERE, 건수 |
| [SQLD-011](SQLD-011.md) | FULL OUTER JOIN 흉내내기 | ★★★☆☆ 중급 | FULL OUTER JOIN, UNION |
| [SQLD-012](SQLD-012.md) | 단일행 서브쿼리 vs 다중행 서브쿼리 | ★★☆☆☆ 초급 | 다중행 서브쿼리, IN, 단일행 연산자 |
| [SQLD-013](SQLD-013.md) | 다중 컬럼 서브쿼리 | ★★★☆☆ 중급 | 다중 컬럼 서브쿼리, 그룹별 최댓값 |
| [SQLD-014](SQLD-014.md) | ORDER BY 절의 스칼라 서브쿼리 | ★★★☆☆ 중급 | 스칼라 서브쿼리, ORDER BY |
| [SQLD-015](SQLD-015.md) | MINUS 를 EXCEPT 로 | ★★☆☆☆ 초급 | MINUS, EXCEPT, 집합 연산 |
| [SQLD-016](SQLD-016.md) | CUBE 흉내내기 | ★★★★☆ 고급 | CUBE, ROLLUP, UNION ALL, GROUPING |
| [SQLD-017](SQLD-017.md) | GROUPING SETS 흉내내기 | ★★★☆☆ 중급 | GROUPING SETS, UNION ALL |
| [SQLD-018](SQLD-018.md) | RATIO_TO_REPORT | ★★☆☆☆ 초급 | RATIO_TO_REPORT, SUM OVER, 비율 |
| [SQLD-019](SQLD-019.md) | 윈도우 프레임 ROWS vs RANGE | ★★★☆☆ 중급 | ROWS, RANGE, 윈도우 프레임, 동점 |
| [SQLD-020](SQLD-020.md) | LAG 의 오프셋과 기본값 | ★★☆☆☆ 초급 | LAG, LEAD, 기본값 |
| [SQLD-021](SQLD-021.md) | EMP 셀프 조인 - 사원과 관리자 | ★★☆☆☆ 초급 | SELF JOIN, EMP, OUTER JOIN |
| [SQLD-022](SQLD-022.md) | EMP 계층형 질의 (CONNECT BY → 재귀 CTE) | ★★★★☆ 고급 | 계층형 질의, CONNECT BY, 재귀 CTE, LEVEL |
| [SQLD-023](SQLD-023.md) | EMP 부서별 급여 순위 | ★★☆☆☆ 초급 | RANK, DENSE_RANK, PARTITION BY, EMP |
| [SQLD-024](SQLD-024.md) | 집계 함수 중첩 (MAX(COUNT(*))) | ★★☆☆☆ 초급 | 집계 중첩, 인라인 뷰 |
| [SQLD-025](SQLD-025.md) | 정규 표현식 함수 | ★★☆☆☆ 초급 | REGEXP_SUBSTR, REGEXP_REPLACE, 정규식 |
| [SQLD-026](SQLD-026.md) | 논리 연산자 우선순위 (NOT > AND > OR) | ★★☆☆☆ 초급 | NOT, AND, OR, 우선순위 |
