.header on
SELECT c.name, f1.flight_num as f1_flight_num,
       f1.origin_city as f1_origin_city,
       f1.dest_city as f1_dest_city,
       f1.actual_time as f1_actual_time,
       f2.flight_num as f2_flight_num,
       f2.origin_city as f2_origin_city,
       f2.dest_city as f2_dest_city,
       f2.actual_time as f2_actual_time,
       f1.actual_time + f2.actual_time AS actual_time
FROM FLIGHTS as f1 JOIN FLIGHTS as f2
    JOIN MONTHS as m1 on f1.month_id = m1.mid
    JOIN MONTHS as m2 on f2.month_id = m2.mid
    JOIN CARRIERS as c on f1.carrier_id = c.cid
WHERE f1.origin_city = 'Seattle WA' AND f2.dest_city = 'Boston MA'
AND f1.dest_city = f2.origin_city AND m1.month = 'July' AND
m2.month = 'July' AND f1.day_of_month = 15 AND f2.day_of_month = 15
AND f1.carrier_id = f2.carrier_id
AND f1.actual_time + f2.actual_time < (7*60);

-- query result has 1472 rows
