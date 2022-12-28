--А) какую сумму в среднем в месяц тратит:
-- пользователи в возрастном диапазоне от 18 до 25 лет включительно
-- пользователи в возрастном диапазоне от 26 до 35 лет включительно

SELECT 
	SUM (kore_1_items.price)/
	COUNT (distinct EXTRACT(YEAR FROM date))/
	COUNT (distinct EXTRACT(MONTH FROM date)) AS "от 18 до 25" 
FROM 
	kore_1_users, 
	kore_1_purchases, 
	kore_1_items
WHERE kore_1_users.userId = kore_1_purchases.userId 
AND kore_1_items.itemId = kore_1_purchases.itemId
AND kore_1_users.age BETWEEN 18 AND 25
;

SELECT 
	SUM (kore_1_items.price)/
	COUNT (distinct EXTRACT(YEAR FROM date))/
	COUNT (distinct EXTRACT(MONTH FROM date)) AS "от 26 до 35" 
FROM 
	kore_1_users, 
	kore_1_purchases, 
	kore_1_items
WHERE kore_1_users.userId = kore_1_purchases.userId 
AND kore_1_items.itemId = kore_1_purchases.itemId
AND kore_1_users.age BETWEEN 26 AND 35
;



-- Б) в каком месяце года выручка от пользователей в возрастном диапазоне 35+ самая большая

WITH 
month_db AS (
	SELECT
		purchaseId,
		EXTRACT(YEAR FROM date) AS year,
		EXTRACT(MONTH FROM date) AS month
	FROM kore_1_purchases
),
new_db AS(
	SELECT
		e.purchaseId,
		e.userId,
		e.itemId,
		e.date,
		j.year,
		j.month
	FROM kore_1_purchases e
	LEFT JOIN month_db j ON j.purchaseId = e.purchaseId
), 
max_sel AS(	
	SELECT 
		new_db.year, 
		new_db.month, 
		SUM(kore_1_items.price)
	FROM 
		kore_1_items, 
		kore_1_users, 
		new_db
	WHERE kore_1_users.userId = new_db.userId 
	AND kore_1_items.itemId = new_db.itemId
	AND kore_1_users.age > 35
	GROUP BY new_db.year, new_db.month
	ORDER BY new_db.year, new_db.month
)
SELECT 
	year, 
	(array_agg(month ORDER BY sum DESC))[1] AS month, 
	MAX(sum) 
FROM max_sel
GROUP BY year
;



-- В) какой товар обеспечивает дает наибольший вклад в выручку за последний год

WITH 
month_db AS (
	SELECT
		purchaseId,
		EXTRACT(YEAR FROM date) AS year
	FROM kore_1_purchases
),
new_db AS(
	SELECT
		e.purchaseId,
		e.userId,
		e.itemId,
		e.date,
		j.year
	FROM kore_1_purchases e
	LEFT JOIN month_db j ON j.purchaseId = e.purchaseId
),
max_item AS(
	SELECT 
		kore_1_Items.itemId, 
		SUM(kore_1_Items.price) 
	FROM 
		kore_1_Items, 
		new_db
	WHERE kore_1_Items.itemId = new_db.itemId 
	AND year = 2021
	GROUP BY kore_1_Items.itemId
)
SELECT * FROM max_item
WHERE sum = (
	SELECT MAX(sum)
	FROM max_item);



-- Г) топ-3 товаров по выручке и их доля в общей выручке за любой год

WITH 
month_db AS (
	SELECT
		purchaseId,
		EXTRACT(YEAR FROM date) AS year
	FROM kore_1_purchases
),
new_db AS(
	SELECT
		e.purchaseId,
		e.userId,
		e.itemId,
		e.date,
		j.year
	FROM kore_1_purchases e
	LEFT JOIN month_db j ON j.purchaseId = e.purchaseId
),
max_item AS(
	SELECT 
		kore_1_Items.itemId, 
		SUM(kore_1_Items.price) AS sum_it
	FROM 
		kore_1_Items, 
		new_db
	WHERE kore_1_Items.itemId = new_db.itemId 
	AND year = 2021
	GROUP BY kore_1_Items.itemId
	ORDER BY sum_it DESC
	LIMIT 3
),
full_sel AS(
	SELECT
		SUM (kore_1_Items.price) AS full_price
	FROM 
		kore_1_Items, 
		new_db
	WHERE kore_1_Items.itemId = new_db.itemId 
	AND year = 2021
)
SELECT 
	itemId, 
	sum_it, 
	sum_it/full_price::decimal*100 AS percent 
FROM 
	max_item, 
	full_sel
;