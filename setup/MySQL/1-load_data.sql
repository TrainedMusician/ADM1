LOAD DATA INFILE '/var/lib/mysql-files/region.tbl' INTO TABLE region FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/nation.tbl' INTO TABLE nation FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/supplier.tbl' INTO TABLE supplier FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/customer.tbl' INTO TABLE customer FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/part.tbl' INTO TABLE part FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/partsupp.tbl' INTO TABLE partsupp FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/orders.tbl' INTO TABLE orders FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';
LOAD DATA INFILE '/var/lib/mysql-files/lineitem.tbl' INTO TABLE lineitem FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';