-- SQL Query
WITH direct_cities AS 
    (SELECT *
    FROM FLIGHTS AS f1
    WHERE f1.origin_city = 'Seattle WA')

SELECT DISTINCT(f.dest_city) AS city
FROM FLIGHTS AS f
WHERE 
    f.origin_city != 'Seattle WA'
    AND f.dest_city NOT IN (SELECT DISTINCT(f2.dest_city) FROM FLIGHTS as f2
                            WHERE f2.origin_city IN (SELECT dest_city from direct_cities))
    AND f.dest_city != 'Seattle WA'
ORDER BY city;

/*

Number of rows my query returns: 3
Total execution time: 00:00:13.493

Output:
Devils Lake ND
Hattiesburg/Laurel MS
St. Augustine FL

*/