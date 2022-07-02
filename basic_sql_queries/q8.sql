.header on
 SELECT c.name, SUM(f.departure_delay) AS delay
 FROM FLIGHTS as f JOIN CARRIERS as c on f.carrier_id = c.cid
 GROUP BY c.name;

-- query result has 22 rows
