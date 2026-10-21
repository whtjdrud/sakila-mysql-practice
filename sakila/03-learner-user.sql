-- 웹 풀이 앱용 읽기 전용 계정 (실수로 데이터가 바뀌지 않도록 SELECT 만 허용)
CREATE USER IF NOT EXISTS 'learner'@'%' IDENTIFIED BY 'learner';
GRANT SELECT, SHOW VIEW ON sakila.* TO 'learner'@'%';
FLUSH PRIVILEGES;
