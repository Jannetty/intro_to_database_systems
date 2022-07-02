-- SQL QUERY:
SELECT DISTINCT(f.origin_city) as city
FROM FLIGHTS as f 
WHERE f.origin_city NOT IN(SELECT DISTINCT(f1.origin_city) 
                    from FLIGHTS as f1
                    WHERE f1.actual_time >= 180 AND f1.canceled = 0)
ORDER BY f.origin_city;

/*

Number of rows my query returns: 109
Total execution time: 00:00:08.231 

First 20 rows of result:
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA

*/
