SELECT c.name      AS category,
       COUNT(*)    AS film_count
FROM category c
JOIN film_category fc ON fc.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY film_count DESC, category;
