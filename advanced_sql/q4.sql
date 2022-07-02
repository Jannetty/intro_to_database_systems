--SQL Query
WITH direct_cities AS 
    (SELECT DISTINCT(f1.dest_city) as dest_city
    FROM FLIGHTS as f1
    WHERE f1.origin_city = 'Seattle WA')

SELECT DISTINCT(f.dest_city) AS city
FROM FLIGHTS as f
WHERE f.origin_city IN (SELECT dest_city FROM direct_cities)
    AND f.dest_city NOT IN (SELECT dest_city FROM direct_cities)
    AND f.dest_city != 'Seattle WA'
ORDER BY city;

/*

Number of rows my query returns: 256
Total execution time: 00:00:11.722

First 20 rows of result:
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME

*/