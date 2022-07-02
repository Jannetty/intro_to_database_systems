# Advanced SQL Queries
These queries were run on an SQL Server on [Windows Azure](https://azure.microsoft.com/en-us/). Data were 1148675 flights from the
 [Bureau of Transportation Statistics](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time) dataset. The subset of flights used is unfortunately no longer publically available. *Data files are not included in this repository and therefore these queries will not run*. The first 20 rows of output from queries is commented in each file. Queries were written using the [SQL Server extension for Visual Studio Code](https://docs.microsoft.com/en-us/sql/tools/visual-studio-code/sql-server-develop-use-vscode?view=sql-server-ver15)

 ## Overview of files
 | File Name | Description |
 | :-------: | :---------- |
 | *[q1.sql](q1.sql)* | Query that, for each origin city, finds the destination city (or cities) with the longest direct flight. Direct flight means a flight with no intermediate stops. Longest flight judged in time, not distance. Names the output columns *origin_city*, *dest_city*, and *time*. Does not include duplicates of the same origin/destination city pair. Orders the result by origin_city and then dest_city (ascending, i.e. alphabetically). |
 |*[q2.sql](q2.sql)* | Query that finds all origin cities that only serve flights shorter than 3 hours. Does not include cancelled flights in determination. Names the output column *city* and sorts rows in ascending order alphabetically. Lists each city only once in the result. |
 |*[q3.sql](q3.sql)*| Query that, for each origin city, finds the percentage of departing flights shorter than 3 hours. Does not include cancelled flights in determination. Names the output columns *origin_city* and *percentage*. Orders by percentage value, then city, ascending. Handles cities without any flights shorter than 3 hours such that these cities return 0. Reports percentages as percentages not decimals (e.g., reports 75.2534 rather than 0.752534). Does not round the percentages. |
 |*[q4.sql](q4.sql)*| Query that lists all cities that can be reached from Seattle through one stop (i.e., with any two flights that go through an intermediate city) but cannot be reached through a direct flight. Does not include Seattle as one of these destinations (even though one could get back with two flights). Names the output column *city*. Orders the output ascending by city. |
 |*[q5.sql](q5.sql)*| Query that lists all cities that cannot be reached from Seattle through a direct flight nor with one stop (i.e., with any two flights that go through an intermediate city). Names the output column *city*. Orders the output ascending by city. |
 |*[q6.sql](q6.sql)*| Query that lists the names of carriers that operate flights from Seattle to San Francisco, CA. Returns each carrier's name only once. Uses a nested query. Name the output column *carrier*. Orders the output ascending by carrier. |
 |*[q7.sql](q7.sql)*| Query that addresses same question as [q6.sql](q6.sql), but does so without using a nested query. Again, names the output column *carrier* and orders ascending by carrier. |
 |*[pros_and_cons_of_public_cloud.txt](pros_and_cons_of_public_cloud.txt)* | A few brief thoughts on the pros and cons of storing databases in public clouds. |


