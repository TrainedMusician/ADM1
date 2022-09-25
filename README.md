# ADM1

## Setup

### MonetDB (Ubuntu)
1. Install [MonetDB](https://www.monetdb.org/easy-setup/) on your system and create a database
2. Copy the data directory to the `/data/` on your system. Or edit the *absolute* paths in `setup/MonetDB/1-load_data.sql`
3. Create a new database called `ADM`
4. Create a user with username: `ADM`, password: `1st@sigmEnt` (or change the credentials in queryExecuter.py)
5. Connect to your newly created database and load the 3 files from `setup/MonetDB/` in ascending order
6. You've successfully loaded in the data :D

### MySQL (Ubuntu)
1. Follow the steps mentioned [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)
2. Create a database `ADM` with a user `ADM`, password `1st@sigmEnt` which should have the following rights:
- SELECT
- CREATE (view)
- DROP (view)


Python is used to execute the queries and compare the DBMS's
## Install Python
1. Install Python 3.10 from [python.org](https://python.org/downloads)
2. Install the following packages:
- matplotlib
- numpy
- pandas
- pymonetdb
- scipy


## Run queries
1. run `python queryExecuter.py {test_system} {DBMS} {scale_factor}` from the `queries/` directory. This will create 23 result files in `results/{system}/{DBMS}/SF-{scale_factor}/`
    There are 22 valid queries which will be checked, the 23rd is a dummy query to ensure that the validating process works.