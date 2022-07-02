-- 1. Create table and load data:
CREATE TABLE frumble(
  name VARCHAR(100),
  discount VARCHAR(4),
  month VARCHAR(3),
  price int
);

.separator \t
.import mrFrumbleData.txt frumble

DELETE FROM frumble
WHERE name = 'name';

--------------------------------------------------------------------------------
-- 2. Find all non-trivial functional dependencies in the database:
SELECT "Months where there is more than one value for discount:";
WITH num_distinct_discounts_per_month AS(
  SELECT f.month as month, COUNT(DISTINCT(f.discount)) as distinct_discounts_per_month
  FROM frumble as f
  GROUP BY f.month
  ORDER BY f.month
)
SELECT * FROM num_distinct_discounts_per_month as nddpm
WHERE nddpm.distinct_discounts_per_month != 1;
-- Output cardinality 0
-- Month implies discount (there is only one value for discount each
-- month). Month and discount are a functional dependency.

SELECT "Items where there is more than one value for price:";
WITH num_distinct_prices_per_item AS(
  SELECT f.name as item, COUNT(DISTINCT(f.price)) as distinct_price_per_item
  FROM frumble as f
  GROUP BY f.name
  ORDER BY f.name
)
SELECT * FROM num_distinct_prices_per_item as ndppi
WHERE ndppi.distinct_price_per_item != 1;
-- Output cardinality 0
-- Name implies price (there is only one value for price for each item name).
-- Name and Price are a functional dependency.

SELECT "Discount percentages where there is more than one value for name
(and COUNT of name values associated with each percentage):";
WITH num_distinct_names_per_discount AS(
  SELECT f.discount as discount, COUNT(DISTINCT(f.name)) as distinct_names_per_discount
  FROM frumble as f
  GROUP BY f.discount
  ORDER BY f.discount
)
SELECT * FROM num_distinct_names_per_discount as ndnpd
WHERE ndnpd.distinct_names_per_discount != 1;
-- Output cardinality 3. There are 36 different values of name for the three
-- values for discount. There are also 36 different names, which means each
-- of the discounts is at one point applied to each of the items for sale.
-- There is no functional dependency between discount and name.

/*
Becacuse we know that month -> discount, and name -> price, and name does not
have a functional dependency on discount, we know by the transitive rule that
month can not have a functional dependency on name or price and discount can not
have a functional dependency on price (in order for any of those functional
dependencies to exist, name and discount would have to be functionally dependent)

From these functional dependencies we can conclude by the transitive property
that (month, name) -> (discount, price).

We have therefore found all of the non-trivial functional dependencies in the
database: (month -> discount), (name -> price), (month, name) -> (discount, price)
*/

--------------------------------------------------------------------------------
-- 3. Decompose the table into BCNF and create SQL tables for decomposed schema:

CREATE TABLE ItemSaleMonth(
  name VARCHAR(100),
  month VARCHAR(3)
);

CREATE TABLE Prices(
  name VARCHAR(100) REFERENCES ItemSaleMonth(name),
  price int
);

CREATE TABLE MonthSaleAmount(
  month VarChar(3) REFERENCES ItemSaleMonth(month),
  discount VARCHAR(4)
);

--------------------------------------------------------------------------------
-- 4. SQL Queries that load new tables and count the size of the tables after
--    loading:

INSERT INTO ItemSaleMonth SELECT frumble.name, frumble.month FROM frumble;

INSERT INTO Prices
  SELECT f.name as name, f.price as price
  FROM frumble as f
  GROUP BY f.name, f.price
  ORDER BY f.name;

INSERT INTO MonthSaleAmount
  SELECT f.month as month, f.discount as discount
  FROM frumble as f
  GROUP BY f.month, f.discount
  ORDER BY f.month;

SELECT("Length of ItemSaleMonth:");
SELECT COUNT(*) FROM ItemSaleMonth; -- 426 (one for each tuple in frumble)
SELECT("Length of Prices:");
SELECT COUNT(*) FROM Prices; -- 36 (one for each name)
SELECT("Length of MonthSaleAmount:");
SELECT COUNT(*) FROM MonthSaleAmount; -- 12 (one for each month)
