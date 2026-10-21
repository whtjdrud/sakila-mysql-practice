SELECT f.film_id,
       f.title,
       c.name AS category
FROM film f
LEFT JOIN inventory i     ON i.film_id      = f.film_id
JOIN film_category fc     ON fc.film_id     = f.film_id
JOIN category c           ON c.category_id  = fc.category_id
WHERE i.inventory_id IS NULL
ORDER BY f.film_id;
