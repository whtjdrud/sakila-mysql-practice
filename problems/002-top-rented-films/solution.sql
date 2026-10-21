SELECT f.title,
       f.rating,
       COUNT(r.rental_id) AS rental_count
FROM rental r
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f      ON f.film_id      = i.film_id
GROUP BY f.film_id, f.title, f.rating
ORDER BY rental_count DESC, f.title
LIMIT 10;
