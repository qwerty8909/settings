-- 01 --
SELECT 
	model, 
	speed, 
	hd 
FROM PC
WHERE price < 500

-- 02 --
SELECT 
	DISTINCT maker 
FROM Product
WHERE type = 'Printer'

-- 03 --
SELECT 
	model, 
	ram, 
	screen
FROM Laptop
WHERE price > 1000

-- 04 --
SELECT *
FROM Printer
WHERE color = 'y'

-- 05 --
SELECT 
	model, 
	speed, 
	hd
FROM PC
WHERE price < 600
AND (cd = '12x' OR cd = '24x')

-- 06 --
SELECT 
	DISTINCT e.Maker, 
	j.speed
FROM 
	Product e, 
	Laptop j
WHERE e.model = j.model
AND j.hd >= 10
-- or --
SELECT 
	DISTINCT e.Maker, 
	j.speed
FROM Product e 
INNER JOIN Laptop j 
	ON e.model = j.model
AND j.hd >= 10

-- 07 --
SELECT 
	DISTINCT e.model, 
	j.price
FROM Product e 
INNER JOIN PC j 
	ON e.model = j.model
WHERE maker = 'B'
UNION ALL
SELECT 
	DISTINCT e.model, 
	j.price
FROM Product e 
INNER JOIN Laptop j 
	ON e.model = j.model
WHERE maker = 'B'
UNION ALL
SELECT 
	DISTINCT e.model, 
	j.price
FROM Product e 
INNER JOIN Printer j 
	ON e.model = j.model
WHERE maker = 'B'

-- 08 --
SELECT 
	DISTINCT e.Maker
FROM Product e 
WHERE e.type = 'PC'
AND e.Maker NOT IN (
SELECT 
	DISTINCT e.Maker
FROM Product e 
WHERE e.type = 'Laptop'
)

-- 09 --
SELECT 
	DISTINCT e.Maker
FROM Product e 
INNER JOIN PC j 
	ON e.model = j.model
WHERE j.speed >= 450

-- 10 --
SELECT 
	DISTINCT model, 
	price
FROM Printer
WHERE price = (
SELECT MAX(price) 
FROM Printer
)

-- 11 --
SELECT 
	AVG (speed) AS Avg_speed
FROM PC

-- 12 --
SELECT 
	AVG (speed) AS Avg_speed
FROM Laptop
WHERE price > 1000

-- 13 --
SELECT 
	AVG (e.speed) AS Avg_speed
FROM 
	PC e, 
	Product j
WHERE e.model = j.model
AND j.maker = 'A'

-- 14 --
SELECT 
	e.class, 
	j.name, 
	e.country
FROM Classes e 
INNER JOIN Ships j 
	ON e.class = j.class
WHERE e.numGuns >= 10

-- 15 --
SELECT 
	DISTINCT hd
FROM PC
GROUP BY hd 
HAVING COUNT(model) >= 2

-- 16 --
SELECT 
	DISTINCT e.model, 
	j.model, 
	e.speed, 
	e.ram
FROM PC e
INNER JOIN PC j 
	ON e.speed= j.speed
WHERE e.ram = j.ram
AND e.model > j.model

-- 17 --
SELECT 
	DISTINCT e.type, 
	e.model, 
	j.speed
FROM 
	Product e, 
	Laptop j
WHERE e.model= j.model
AND j.speed < (
SELECT MIN(speed) 
FROM PC
)

-- 18 --
SELECT 
	DISTINCT e.maker, 
	j.price
FROM Product e
INNER JOIN Printer j 
	ON e.model= j.model
WHERE j.color = 'Y'
AND j.price = (
SELECT MIN(price) 
FROM Printer 
WHERE color = 'Y'
)

-- 19 --
SELECT 
	e.maker, 
	AVG (j.screen) AS Avg_screen
FROM Product e
INNER JOIN Laptop j 
	ON e.model= j.model
GROUP BY e.maker

-- 20 --
SELECT 
	e.maker, 
	COUNT (e.model) AS Count_Model
FROM Product e
WHERE e.type = 'PC'
GROUP BY e.maker
HAVING COUNT(e.model) >= 3

-- 21 --
SELECT 
	e.maker, 
	MAX (j.price) AS Max_price
FROM Product e
INNER JOIN PC j 
	ON e.model= j.model
GROUP BY e.maker

-- 22 --
SELECT 
	e.speed, 
	AVG (e.price) AS Avg_price
FROM PC e 
WHERE e.speed > 600
GROUP BY e.speed

-- 23 --
SELECT 
	DISTINCT e.maker
FROM Product e 
INNER JOIN PC j 
	ON e.model= j.model
WHERE j.speed >= 750
AND e.maker IN (
SELECT 
	DISTINCT e.maker
FROM Product e 
INNER JOIN Laptop j 
	ON e.model= j.model
WHERE j.speed >= 750
)

-- 24 --
WITH cte0 AS(
SELECT 
	e.model, 
	e.price
FROM PC e
WHERE e.price = (SELECT MAX(price) FROM PC)
UNION ALL
SELECT 
	j.model, 
	j.price
FROM Laptop j
WHERE j.price = (SELECT MAX(price) FROM Laptop)
UNION ALL
SELECT 
	i.model, 
	i.price
FROM Printer i
WHERE i.price = (SELECT MAX(price) FROM Printer)
)
SELECT DISTINCT model 
FROM cte0
WHERE price = (SELECT MAX(price) FROM cte0)

-- 25 --
SELECT DISTINCT e.maker
FROM Product e
WHERE e.maker IN (
SELECT e.maker
FROM product e
WHERE e.type='printer'
)
AND e.model IN (
SELECT j.model
FROM PC j
WHERE j.ram = (SELECT MIN(ram) FROM PC)
AND j.speed = (SELECT MAX(speed) FROM PC WHERE ram = (SELECT MIN(ram) FROM PC))
)

-- 26 --
WITH cte0 AS (
SELECT 
	e.model, 
	e.price 
FROM PC e
UNION ALL
SELECT 
	j.model, 
	j.price 
FROM Laptop j
)
SELECT AVG(price) AS AVG_price
FROM Product
INNER JOIN cte0 
	ON Product.model=cte0.model
WHERE Product.maker='A'

-- 27 --
SELECT e.maker, AVG (hd) AS Avg_hd
FROM Product e
INNER JOIN PC j
	ON e.model=j.model
WHERE e.maker IN (
SELECT e.maker
FROM product e
WHERE e.type='printer'
)
GROUP BY e.maker

-- 28 --
WITH cte0 AS (
SELECT COUNT(e.maker) AS col
FROM Product e
GROUP BY e.maker
)
SELECT COUNT(col) AS qty
FROM cte0
WHERE col = (SELECT MIN(col) FROM cte0)

-- 29 --
SELECT 
	e.point, 
	e.date, 
	e.inc, 
	j.out
FROM Income_o e 
LEFT JOIN Outcome_o j
	ON e.date=j.date AND e.point=j.point
UNION
SELECT 
	j.point, 
	j.date, 
	e.inc, 
	j.out
FROM Income_o e 
RIGHT JOIN Outcome_o j
	ON e.date=j.date AND e.point=j.point

-- 30 --
WITH cte0 AS (
SELECT 
	point, 
	date, 
	SUM(out) AS Outcome
FROM outcome
GROUP BY point, date
), 
cte1 AS (
SELECT 
	point, 
	date, 
	SUM(inc) AS income
FROM income
GROUP BY point, date
)
SELECT 
	e.point, 
	e.date, 
	j.Outcome, 
	e.income
FROM cte1 e 
LEFT JOIN cte0 j
	ON e.date=j.date AND e.point=j.point
UNION
SELECT 
	j.point, 
	j.date, 
	j.Outcome, 
	e.income
FROM cte1 e 
RIGHT JOIN cte0 j
	ON e.date=j.date AND e.point=j.point

-- 31 --
SELECT 
	class, 
	country
FROM Classes
WHERE bore >= 16

-- 32 --
WITH cte0 AS (
SELECT 
	j.name, 
	e.class, 
	e.country, 
	e.bore
FROM 
	Classes e, 
	Ships j 
WHERE e.class = j.class
UNION
SELECT 
	j.ship AS name, 
	e.class, 
	e.country, 
	e.bore 
FROM 
	Classes e, 
	Outcomes j
WHERE e.class = j.ship
)
SELECT 
	country, 
	CAST(AVG(POWER(bore,3)/2) AS decimal(10,2)) AS weight
FROM cte0
GROUP BY country

-- 33 --
SELECT ship
FROM Outcomes
WHERE result = 'sunk'
AND battle = 'North Atlantic'

-- 34 --
SELECT e.name
FROM Ships e, Classes j
WHERE e.class = j.class
AND e.launched >= 1922
AND j.displacement > 35000
AND j.type = 'bb'

-- 35 --
SELECT 
	model, 
	type
FROM Product
WHERE model NOT LIKE '%[^0-9]%'
OR model NOT LIKE '%[^a-z]%'

-- 36 --
SELECT e.name
FROM Ships e
INNER JOIN Classes j
ON e.name = j.class
UNION
SELECT i.ship AS name 
FROM Outcomes i
INNER JOIN Classes j 
ON i.ship = j.class

-- 37 --
WITH cte0 AS (
SELECT 
	e.class, 
	e.name 
FROM Ships e
UNION
SELECT 
	j.class, 
	i.ship 
FROM Classes j
INNER JOIN Outcomes i 
ON j.class=i.ship
) 
SELECT class 
FROM cte0
GROUP BY class
HAVING COUNT(class)=1

-- 38 --
WITH cte0 AS (
SELECT DISTINCT country 
FROM Classes 
WHERE type ='bb'
),
cte1 AS (
SELECT DISTINCT country 
FROM Classes 
WHERE type ='bc'
)
SELECT e.country
FROM cte0 e
INNER JOIN cte1 j
ON e.country = j.country
-- or--
WITH cte0 AS (
SELECT DISTINCT country 
FROM Classes 
WHERE type ='bb'
UNION ALL
SELECT DISTINCT country 
FROM Classes 
WHERE type ='bc'
)
SELECT country 
FROM cte0
GROUP BY country
HAVING COUNT(country) > 1

-- 39 --
SELECT DISTINCT e.ship
FROM Outcomes e 
INNER JOIN Battles j
	ON e.battle=j.name 
AND e.ship IN (
SELECT a.ship
FROM Outcomes a 
INNER JOIN Battles b
	ON a.battle=b.name 
AND a.result = 'damaged' 
AND j.date>b.date)

-- 40 --
SELECT 
	DISTINCT e.maker, 
	e.type
FROM Product e
WHERE e.maker in (
SELECT e.maker 
FROM Product e
GROUP BY e.maker
HAVING COUNT (e.model) > 1
AND COUNT(DISTINCT e.type) = 1
)
-- 41 --
-- 42 --
-- 43 --
-- 44 --
-- 45 --
-- 46 --
-- 47 --
-- 48 --
-- 49 --
-- 50 --
-- 51 --
-- 52 --
-- 53 --
-- 54 --
-- 55 --
-- 56 --
-- 57 --
-- 58 --
-- 59 --
-- 60 --