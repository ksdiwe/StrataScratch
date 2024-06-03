SELECT 
-- shortest tenured count
(SELECT count(id)
FROM uber_employees
WHERE hire_date = most_hire_date and termination_date IS NULL) AS shortest_tenured_count,

-- longest_tenured count
(SELECT count(id)
FROM uber_employees
WHERE hire_date = least_hire_date and termination_date IS NULL) AS longest_tenured_count,

DATEDIFF(most_hire_date, least_hire_date) AS days_diff

FROM
(SELECT 
    MAX(hire_date) AS most_hire_date,
    MIN(hire_date) AS least_hire_date
FROM uber_employees
WHERE termination_date IS NULL) temp
