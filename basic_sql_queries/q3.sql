.header on
SELECT w.day_of_week, AVG(f.arrival_delay) as delay
FROM FLIGHTS as f
JOIN WEEKDAYS as w on f.day_of_week_id = w.did
GROUP BY w.day_of_week
ORDER BY AVG(f.arrival_delay) DESC
LIMIT 1;

-- query result has 1 row
