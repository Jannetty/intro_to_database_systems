.header on
SELECT c.name, AVG(f.canceled)*100 as percentage
FROM FLIGHTS as f
JOIN CARRIERS as c on f.carrier_id = c.cid
WHERE f.origin_city = 'Seattle WA'
GROUP BY c.name
HAVING (AVG(f.canceled) > .005);

-- query result has 6 rows
