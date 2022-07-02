# Basic SQL Queries

Practice writing SQL queries on a relational flights database. Data abridged from [Bureau of Transportation Statistics](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time).

## Running Queries
Data files must be uncompressed from [flight_dataset.zip](flight_dataset.zip). All files in uncompressed flight-dataset directory must be moved into the same directory as .sql files to run queries.

You must have [SQLite 3](https://www.sqlite.org/) installed to run queries.
To run, launch sqlite3:
```bash
$ sqlite3
```
then create and import tables by running:
```bash
sqlite> .read create-tables.sql
sqlite> .read import-tables.sql
```
Queries can then be run using:
```bash
sqlite> .read qX.sql
```

## Overview of data files
| File Name | Description |
| :-------: | :---------- |
|*[flight_dataset.zip](flight_dataset.zip)* | compressed version of all data files. Please uncompress and put files (described below) in same directory as sql files to run queries. |
|*[carriers.csv](carriers.csv)* | carriers and their abbreviations (IDs) |
|*[months.csv](months.csv)* | months and their int abbreviations (IDs)|
|*[weekdays.csv](weekdays.csv)* | weekdays and their int abbreviations (IDs)|
|*[flights-small.csv](flights-small.csv)* | subset of [Bureau of Transportation flight statistics](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time). See schema in FLIGHTS table in [create-tables.sql](create-tables.sql). |

## Overview of SQL files
| File Name | Description |
| :-------: | :---------- |
| *[create-tables.sql](create-tables.sql)* | creates tables to store data from data files. See this file to see data file (and table) schemas. |
| *[import-tables.sql](import-tables.sql)* | imports data from data files into tables created in [create-tables.sql](create-tables.sql) |
| *[q1.sql](q1.sql)* | Query that lists the distinct flight numbers of all flights from Seattle to Boston by Alaska Airlines Inc. on Mondays. Uses the flight_num column instead of fid. Names the output column *flight_num*.|
| *[q2.sql](q2.sql)* |  Query that finds all itineraries from Seattle to Boston on July 15th that have one stop (i.e., flight 1: Seattle -> [somewhere], flight2: [somewhere] -> Boston) and that have a total flight time (actual_time) of less than 7 hours. Both flights must depart on the same day (same day here means the date of flight) and must be with the same carrier. It's fine if the landing date is different from the departing date (i.e., in the case of an overnight flight). Doesn't check whether the first flight overlaps with the second one since the departing and arriving time of the flights are not provided. For each itinerary, the query returns the name of the carrier, the first flight number, the origin and destination of that first flight, the flight time, the second flight number, the origin and destination of the second flight, the second flight time, and finally the total flight time. Only counts flight times here; does not include any layover time. Names the output columns *name* (as in the name of the carrier), *f1_flight_num*, *f1_origin_city*, *f1_dest_city*, *f1_actual_time*, *f2_flight_num*, *f2_origin_city*, *f2_dest_city*, *f2_actual_time*, and *actual_time* as the total flight time. Lists the output columns in this order.|
| *[q3.sql](q3.sql)* |  Query that finds the day of the week with the longest average arrival delay. Returns the name of the day and the average delay. Names the output columns *day_of_week* and *delay*, and returns them in that order. |
| *[q4.sql](q4.sql)* | Query that finds the names of all airlines that ever flew more than 1000 flights in one day (i.e., a specific day/month, but not any 24-hour period). Returns only the names of the airlines. Does not return any duplicates (i.e., airlines with the exact same name). Names the output column *name*. |
| *[q5.sql](q5.sql)* | Query that finds all airlines that had more than 0.5% (= 0.005) of their flights out of Seattle canceled. Returns the name of each airline and the percentage of canceled flights out of Seattle. Percentages are outputted in percent format (3.5% as 3.5 not 0.035). Orders results by the percentage of canceled flights in ascending order. Names the output columns *name* and *percentage*, and returns them in that order|
| *[q6.sql](q6.sql)* | Query that finds the maximum price of tickets between Seattle and New York, NY (i.e. Seattle to NY or NY to Seattle). Shows the maximum price for each airline separately. Names the output columns *carrier* and *max_price*, and returns them in that order.|
| *[q7.sql](q7.sql)* | Query that finds the total capacity of all direct flights that fly between Seattle and San Francisco, CA on July 10th (i.e. Seattle to SF or SF to Seattle). Names the output column *capacity*. |
| *[q8.sql](q8.sql)* | Query that computes the total departure delay of each airline across all flights. Some departure delays may be negative (indicating an early departure); they are included and reduce the total. Names the output columns *name* and *delay*, and returns them in that order.|
