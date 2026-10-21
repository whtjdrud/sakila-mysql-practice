SELECT s.store_id,
       DATE_FORMAT(p.payment_date, '%Y-%m') AS month,
       COUNT(*)                             AS payments,
       SUM(p.amount)                        AS revenue
FROM payment p
JOIN staff s ON s.staff_id = p.staff_id
GROUP BY s.store_id, month
ORDER BY s.store_id, month;
