-- SQL Query
SELECT c.name as carrier
FROM CARRIERS as c 
WHERE c.cid IN (
    SELECT DISTINCT(f.carrier_id)
    FROM FLIGHTS as f 
    WHERE (f.origin_city = 'Seattle WA' AND f.dest_city = 'San Francisco CA') OR
            (f.origin_city = 'San Fransisco CA' AND f.dest_city = 'Seattle WA')
)
ORDER BY c.name 

/*

Number of rows my query returns: 4
Total execution time: 00:00:01.862

Result:
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America

*/