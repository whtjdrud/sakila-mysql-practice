WITH totals AS (
    SELECT c.customer_id,
           CONCAT(c.first_name, ' ', c.last_name) AS customer,
           co.country,
           SUM(p.amount) AS total_paid
    FROM payment p
    JOIN customer c ON c.customer_id = p.customer_id
    JOIN address a  ON a.address_id  = c.address_id
    JOIN city ci    ON ci.city_id    = a.city_id
    JOIN country co ON co.country_id = ci.country_id
    GROUP BY c.customer_id, customer, co.country
), ranked AS (
    SELECT customer, country, total_paid,
           RANK() OVER (ORDER BY total_paid DESC)                      AS overall_rank,
           RANK() OVER (PARTITION BY country ORDER BY total_paid DESC) AS country_rank
    FROM totals
)
SELECT *
FROM ranked
WHERE overall_rank <= 10
ORDER BY overall_rank, customer;
