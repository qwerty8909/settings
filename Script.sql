create table de11an.kore_empty_table (id integer);

alter table de11an.kore_empty_table 
add column text_col varchar(20);

alter table de11an.kore_empty_table
alter column text_col type VARCHAR(15);

DELETE FROM de11an.kore_empty_table WHERE id = 12345;

insert into de11an.kore_empty_table(text_col) 
values ('Hello, world!');

UPDATE de11an.kore_empty_table
SET id = 12345 WHERE text_col = 'Hello, world!';

alter table de11an.kore_empty_table 
alter column text_col type varchar(10) using text_col::varchar(10);

select * from de11an.kore_empty_table

select first_name, last_name,
	case
		when salary < 4000 then 'бедные'
		when salary >= 4000 and salary < 8000 then 'средний класс'
		when salary >= 8000 and salary < 20000 then 'богатые'
		else 'очень богатые'
	end as class_
from hr.employees;

SELECT  
	last_name, 
	first_name, 
	commission_pct, 
	salary 											AS salary_before, 
	salary+100000*COALESCE(commission_pct, 0) 		AS salary_after,
	CASE
		WHEN salary < 4000 THEN 'бедные'
		WHEN salary < 8000 THEN 'средний класс'
		WHEN salary < 20000 THEN 'богатые'
		ELSE 'очень богатые'
	END 											AS class_before,
	CASE
		WHEN salary+100000*COALESCE(commission_pct, 0) < 4000 THEN 'бедные'
		WHEN salary+100000*COALESCE(commission_pct, 0) < 8000 THEN 'средний класс'
		WHEN salary+100000*COALESCE(commission_pct, 0) < 20000 THEN 'богатые'
		ELSE 'очень богатые'
	END 											AS class_after
FROM 
	hr.employees;


-- explain перед запросом чтоб посмотреть план


WITH cte0 AS(
	SELECT
		employee_id,
		salary 											AS salary_before,
		salary+100000*COALESCE(commission_pct, 0) 		AS salary_after
	FROM
		hr.employees
),
cte1 AS(
	SELECT 
		e.last_name,
		e.first_name,
		e.commission_pct,
		j.salary_before,
		j.salary_after,
		CASE
			WHEN salary_before < 4000 THEN 'бедные'
			WHEN salary_before < 8000 THEN 'средний класс'
			WHEN salary_before < 20000 THEN 'богатые'
			ELSE 'очень богатые'
		END 											AS class_before,
		CASE
			WHEN salary_after < 4000 THEN 'бедные'
			WHEN salary_after < 8000 THEN 'средний класс'
			WHEN salary_after < 20000 THEN 'богатые'
			ELSE 'очень богатые'
		END 											AS class_after
	FROM 
		hr.employees e
	LEFT JOIN cte0 j ON j.employee_id = e.employee_id
)
SELECT  
	last_name, 
	first_name, 
	commission_pct, 
	salary_before, 
	cte1.class_before,
	salary_after,
	cte1.class_after
FROM 
	cte1
WHERE
	cte1.class_before <> cte1.class_after
;








select
	*
from
	hr.departments d 
where department_id in (
	select
		department_id
	from
		hr.employees e
	group by department_id
	having count(*) > (
		select
			avg(count_depar) 
		from (
			select
				department_id,
				count(*) as count_depar
			from hr.employees e
			group by department_id
		) a
	)
);

with avg_emp as (
    select
        avg(count) as avg_emp
    from (
        select
            department_id,
            count(*) as count
        from hr.employees
        group by department_id
    ) a
),
dep_names as (
    select
        department_id,
        department_name
    from hr.departments
)
select
    department_id,
    count(*) as count
from hr.employees
group by department_id
having count(*) > (select avg_emp from avg_emp);


