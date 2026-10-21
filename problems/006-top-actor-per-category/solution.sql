WITH actor_revenue AS (
    SELECT cat.name AS category,
           a.actor_id,
           CONCAT(a.first_name, ' ', a.last_name) AS actor,
           SUM(p.amount) AS revenue
    FROM payment p
    JOIN rental r         ON r.rental_id     = p.rental_id
    JOIN inventory i      ON i.inventory_id  = r.inventory_id
    JOIN film_category fc ON fc.film_id      = i.film_id
    JOIN category cat     ON cat.category_id = fc.category_id
    JOIN film_actor fa    ON fa.film_id      = i.film_id
    JOIN actor a          ON a.actor_id      = fa.actor_id
    GROUP BY cat.name, a.actor_id, actor
), ranked AS (
    SELECT *, RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
    FROM actor_revenue
)
SELECT category, actor, revenue
FROM ranked
WHERE rnk = 1
ORDER BY category, actor;
