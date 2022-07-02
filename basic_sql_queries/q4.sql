.header on
SELECT DISTINCT(c.name)
FROM FLIGHTS as f
     JOIN CARRIERS as c on f.carrier_id = c.cid
     JOIN MONTHS as m on f.month_id = m.mid
GROUP BY c.name, m.month, f.day_of_month
HAVING count(f.fid) > 1000;

-- query result has 12 rows
