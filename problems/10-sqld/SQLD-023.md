# SQLD-023. EMP 부서별 급여 순위

**유형:** SQLD 유형 · **난이도:** ★★☆☆☆ 초급 · **태그:** `RANK` `DENSE_RANK` `PARTITION BY` `EMP`

## 문제

SQLD-021 의 `emp` CTE 를 사용해 부서별 급여 순위를 구하세요.

- 출력: `deptno`, `ename`, `sal`, `rnk`(RANK), `dense_rnk`(DENSE_RANK), `dept_max`(부서 최고 급여)
- 정렬: `deptno`, `sal` 내림차순, `ename` 순

<details>
<summary>정답 쿼리 보기</summary>

```sql
WITH emp(empno, ename, job, mgr, sal, deptno) AS (
    SELECT 7839,'KING','PRESIDENT',NULL,5000,10 UNION ALL SELECT 7566,'JONES','MANAGER',7839,2975,20
    UNION ALL SELECT 7698,'BLAKE','MANAGER',7839,2850,30 UNION ALL SELECT 7782,'CLARK','MANAGER',7839,2450,10
    UNION ALL SELECT 7788,'SCOTT','ANALYST',7566,3000,20 UNION ALL SELECT 7902,'FORD','ANALYST',7566,3000,20
    UNION ALL SELECT 7369,'SMITH','CLERK',7902,800,20 UNION ALL SELECT 7499,'ALLEN','SALESMAN',7698,1600,30
    UNION ALL SELECT 7521,'WARD','SALESMAN',7698,1250,30 UNION ALL SELECT 7654,'MARTIN','SALESMAN',7698,1250,30
    UNION ALL SELECT 7844,'TURNER','SALESMAN',7698,1500,30 UNION ALL SELECT 7900,'JAMES','CLERK',7698,950,30
    UNION ALL SELECT 7876,'ADAMS','CLERK',7788,1100,20 UNION ALL SELECT 7934,'MILLER','CLERK',7782,1300,10
)
SELECT deptno, ename, sal,
       RANK()       OVER (PARTITION BY deptno ORDER BY sal DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY deptno ORDER BY sal DESC) AS dense_rnk,
       MAX(sal)     OVER (PARTITION BY deptno) AS dept_max
FROM emp
ORDER BY deptno, sal DESC, ename;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| deptno | ename | sal | rnk | dense_rnk | dept_max |
|---|---|---|---|---|---|
| 10 | KING | 5000 | 1 | 1 | 5000 |
| 10 | CLARK | 2450 | 2 | 2 | 5000 |
| 10 | MILLER | 1300 | 3 | 3 | 5000 |
| 20 | FORD | 3000 | 1 | 1 | 3000 |
| 20 | SCOTT | 3000 | 1 | 1 | 3000 |
| 20 | JONES | 2975 | 3 | 2 | 3000 |
| 20 | ADAMS | 1100 | 4 | 3 | 3000 |
| 20 | SMITH | 800 | 5 | 4 | 3000 |
| 30 | BLAKE | 2850 | 1 | 1 | 2850 |
| 30 | ALLEN | 1600 | 2 | 2 | 2850 |
| 30 | TURNER | 1500 | 3 | 3 | 2850 |
| 30 | MARTIN | 1250 | 4 | 4 | 2850 |
| 30 | WARD | 1250 | 4 | 4 | 2850 |
| 30 | JAMES | 950 | 6 | 5 | 2850 |

> 총 14행

</details>

## 해설

20번 부서의 SCOTT·FORD(3000) 공동 1위 다음 JONES 는 RANK 3위, DENSE_RANK 2위 — 시험에서 결과표를 고르는 단골 문제입니다.
30번 부서의 WARD·MARTIN(1250) 동점도 같은 방식으로 확인해 보세요.
