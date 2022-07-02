-- SQL Query
WITH MaxLen AS 
    (SELECT DISTINCT(f1.origin_city) as origin_city,
            MAX(f1.actual_time) as max_time
    FROM FLIGHTS as f1
    GROUP BY f1.origin_city)
SELECT  f.origin_city, f.dest_city, f.actual_time as time
FROM    FLIGHTS as f, MaxLen as ml
WHERE   f.origin_city = ml.origin_city
        AND f.actual_time = ml.max_time
GROUP BY f.origin_city, f.dest_city, f.actual_time
ORDER BY f.origin_city, f.dest_city

/*

Number of rows my query returns: 334
Total execution time: 00:00:06.507

First 20 rows of output:
Aberdeen SD	Minneapolis MN	106
Abilene TX	Dallas/Fort Worth TX	111
Adak Island AK	Anchorage AK	471
Aguadilla PR	New York NY	368
Akron OH	Atlanta GA	408
Albany GA	Atlanta GA	243
Albany NY	Atlanta GA	390
Albuquerque NM	Houston TX	492
Alexandria LA	Atlanta GA	391
Allentown/Bethlehem/Easton PA	Atlanta GA	456
Alpena MI	Detroit MI	80
Amarillo TX	Houston TX	390
Anchorage AK	Barrow AK	490
Appleton WI	Atlanta GA	405
Arcata/Eureka CA	San Francisco CA	476
Asheville NC	Chicago IL	279
Ashland WV	Cincinnati OH	84
Aspen CO	Los Angeles CA	304
Atlanta GA	Honolulu HI	649
Atlantic City NJ	Fort Lauderdale FL	212

*/