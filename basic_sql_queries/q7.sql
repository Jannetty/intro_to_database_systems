. header on
SELECT SUM(f.capacity) AS capacity
FROM FLIGHTS as f
     JOIN MONTHS as m on f.month_id = m.mid
WHERE ((f.origin_city = 'San Francisco CA' AND f.dest_city = 'Seattle WA')
OR (f.origin_city = 'Seattle WA' AND f.dest_city = 'San Francisco CA'))
AND m.month = 'July' AND f.day_of_month = 10;

-- query result has 1 row
