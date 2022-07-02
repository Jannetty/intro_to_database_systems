.header on
SELECT c.name as carrier, MAX(f.price) as max_price
FROM FLIGHTS as f
JOIN CARRIERS as c on f.carrier_id = c.cid
WHERE ((f.origin_city = 'New York NY' AND f.dest_city = 'Seattle WA')
OR (f.origin_city = 'Seattle WA' AND f.dest_city = 'New York NY'))
GROUP BY c.name;

-- query result has 3 rows
