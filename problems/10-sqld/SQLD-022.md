# SQLD-022. EMP 계층형 질의 (CONNECT BY → 재귀 CTE)

**유형:** SQLD 유형 · **난이도:** ★★★★☆ 고급 · **태그:** `계층형 질의` `CONNECT BY` `재귀 CTE` `LEVEL`

## 문제

SQLD-021 의 `emp` CTE 를 사용해 Oracle 의 아래 계층형 질의와 같은 결과를 만드세요.

```sql
SELECT LEVEL, LPAD(' ', 4 * (LEVEL - 1)) || ename AS tree,
       SYS_CONNECT_BY_PATH(ename, '/') AS path, CONNECT_BY_ISLEAF AS is_leaf
FROM emp
START WITH mgr IS NULL
CONNECT BY PRIOR empno = mgr
ORDER SIBLINGS BY ename;
```

- 출력: `lvl`, `tree`, `path`, `is_leaf` — 형제끼리 이름순인 **깊이 우선** 순서 (`path` 순으로 정렬하면 됩니다)

<details>
<summary>정답 쿼리 보기</summary>

```sql
WITH RECURSIVE emp(empno, ename, job, mgr, sal, deptno) AS (
    SELECT 7839,'KING','PRESIDENT',NULL,5000,10 UNION ALL SELECT 7566,'JONES','MANAGER',7839,2975,20
    UNION ALL SELECT 7698,'BLAKE','MANAGER',7839,2850,30 UNION ALL SELECT 7782,'CLARK','MANAGER',7839,2450,10
    UNION ALL SELECT 7788,'SCOTT','ANALYST',7566,3000,20 UNION ALL SELECT 7902,'FORD','ANALYST',7566,3000,20
    UNION ALL SELECT 7369,'SMITH','CLERK',7902,800,20 UNION ALL SELECT 7499,'ALLEN','SALESMAN',7698,1600,30
    UNION ALL SELECT 7521,'WARD','SALESMAN',7698,1250,30 UNION ALL SELECT 7654,'MARTIN','SALESMAN',7698,1250,30
    UNION ALL SELECT 7844,'TURNER','SALESMAN',7698,1500,30 UNION ALL SELECT 7900,'JAMES','CLERK',7698,950,30
    UNION ALL SELECT 7876,'ADAMS','CLERK',7788,1100,20 UNION ALL SELECT 7934,'MILLER','CLERK',7782,1300,10
), tree AS (
    SELECT empno, ename, 1 AS lvl, CAST(CONCAT('/', ename) AS CHAR(500)) AS path
    FROM emp WHERE mgr IS NULL
    UNION ALL
    SELECT e.empno, e.ename, t.lvl + 1, CONCAT(t.path, '/', e.ename)
    FROM tree t JOIN emp e ON e.mgr = t.empno
)
SELECT t.lvl,
       CONCAT(REPEAT(' ', 4 * (t.lvl - 1)), t.ename) AS tree,
       t.path,
       NOT EXISTS (SELECT 1 FROM emp c WHERE c.mgr = t.empno) AS is_leaf
FROM tree t
ORDER BY t.path;
```

</details>

<details>
<summary>실행 결과 보기</summary>

| lvl | tree | path | is_leaf |
|---|---|---|---|
| 1 | KING | /KING | 0 |
| 2 |     BLAKE | /KING/BLAKE | 0 |
| 3 |         ALLEN | /KING/BLAKE/ALLEN | 1 |
| 3 |         JAMES | /KING/BLAKE/JAMES | 1 |
| 3 |         MARTIN | /KING/BLAKE/MARTIN | 1 |
| 3 |         TURNER | /KING/BLAKE/TURNER | 1 |
| 3 |         WARD | /KING/BLAKE/WARD | 1 |
| 2 |     CLARK | /KING/CLARK | 0 |
| 3 |         MILLER | /KING/CLARK/MILLER | 1 |
| 2 |     JONES | /KING/JONES | 0 |
| 3 |         FORD | /KING/JONES/FORD | 0 |
| 4 |             SMITH | /KING/JONES/FORD/SMITH | 1 |
| 3 |         SCOTT | /KING/JONES/SCOTT | 0 |
| 4 |             ADAMS | /KING/JONES/SCOTT/ADAMS | 1 |

> 총 14행

</details>

## 해설

| Oracle | MySQL 재귀 CTE |
|---|---|
| `START WITH mgr IS NULL` | 앵커 쿼리의 WHERE |
| `CONNECT BY PRIOR empno = mgr` | 재귀 조인 `e.mgr = t.empno` (부모 → 자식 = **순방향**) |
| `LEVEL` | 재귀마다 +1 하는 컬럼 |
| `SYS_CONNECT_BY_PATH` | 경로 문자열 누적 |
| `CONNECT_BY_ISLEAF` | 자식이 없는지 `NOT EXISTS` |
| `ORDER SIBLINGS BY` | 경로 문자열 정렬 (이름 길이가 다르면 정확하지 않을 수 있음) |
**SQLD 빈출**: `PRIOR` 가 붙은 쪽이 부모입니다. `CONNECT BY PRIOR mgr = empno` 로 바꾸면 **역방향**(자식 → 부모)으로 올라갑니다.
