# Q1
SELECT store_id, address, district, city, country
FROM store, address, country, city
WHERE store.address_id = address.address_id
        AND address.city_id = city.city_id
        AND city.country_id = country.country_id;

# Q2
SELECT CONCAT(first_name, ' ', last_name) as name
FROM actor, film, film_actor
WHERE film.title = 'WEST LION'
        AND actor.actor_id = film_actor.actor_id
        AND film.film_id = film_actor.film_id;

# Q3
SELECT first_name, last_name, SUM(amount) as summation
FROM customer, payment
WHERE payment.customer_id = customer.customer_id
GROUP BY first_name, last_name
ORDER BY summation  DESC
LIMIT 3;

# Q4
SELECT film.film_id, title, SUM(amount) as summation
FROM rental, payment, inventory, film
WHERE film.film_id = inventory.film_id
        AND payment.rental_id = rental.rental_id
        AND rental.inventory_id = inventory.inventory_id
GROUP BY title, film.film_id
ORDER BY summation DESC
LIMIT 1;

# Q5
SELECT actor.actor_id, CONCAT(first_name, ' ', last_name) as name, COUNT(film_actor.film_id) as summation
FROM actor, film_actor
WHERE actor.actor_id = film_actor.actor_id
GROUP BY actor.actor_id, name
HAVING summation > 40;

# Q6
SELECT DISTINCT CONCAT(first_name, ' ', last_name) as name
FROM rental, customer
WHERE rental.customer_id = customer.customer_id
        AND rental.customer_id NOT IN (
            SELECT rental.customer_id
            FROM rental, inventory, film
            WHERE film.title = 'WEST LION'
                    AND film.film_id = inventory.film_id
                    AND inventory.inventory_id = rental.inventory_id
    );

# Q7
SELECT CONCAT(first_name, ' ', last_name) as name
FROM actor
WHERE actor_id = (
    SELECT FA1.actor_id
    FROM film_actor FA1, film_actor FA2
    WHERE FA1.actor_id = FA2.actor_id
            AND FA1.film_id = (
                SELECT film_id
                FROM film
                WHERE title = 'FIRE WOLVES'
            )
            AND FA2.film_id = (
                SELECT film_id
                FROM film
                WHERE title = 'JAWBREAKER BROOKLYN'
            )
    )
;

# Q8
SELECT category.category_id, category.name, COUNT(category.category_id) as amount
FROM film_category, category
WHERE category.category_id = film_category.category_id
GROUP BY category.category_id, category.name;

# Q9
SELECT DISTINCT title
FROM film, inventory I1, inventory I2
WHERE I1.film_id = I2.film_id
        AND I1.store_id <> I2.store_id
        AND I1.film_id = film.film_id;

# Q10
SELECT first_name, last_name, TIMESTAMPDIFF(second , rental_date, return_date) as rental_length
FROM customer, rental
WHERE customer.customer_id = rental.customer_id
ORDER BY rental_length DESC
LIMIT 3;

#Q11
INSERT INTO sakila.customer (store_id, first_name, last_name, email, address_id, create_date)
VALUES (1, 'PINSKY', 'ROBIN', 'xu568059888@gmail.com', 6, NOW());

#Q12
UPDATE customer
SET active = 0
WHERE customer_id = 609;

#Q13
DELETE FROM customer
WHERE customer_id = 608;

