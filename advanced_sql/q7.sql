-- SQL Query
SELECT DISTINCT(c.name) as carrier
FROM FLIGHTS as f JOIN CARRIERS as c ON f.carrier_id = c.cid
WHERE (f.origin_city = 'Seattle WA' AND f.dest_city = 'San Francisco CA') OR
        (f.origin_city = 'San Fransisco CA' AND f.dest_city = 'Seattle WA')
ORDER BY c.name 

/*

Number of rows my query returns: 4
Total execution time: 00:00:02.045

Result:
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America

*/