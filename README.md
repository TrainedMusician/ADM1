# ADM1

## Setup MonetDB
1. Install [MonetDB](https://www.monetdb.org/easy-setup/) on your system and create a database
2. Copy the data directory to the `/data/` on your system. Or edit the *absolute* paths in `setup/MonetDB/1-load_data.SF-1.sql`
3. Connect to your newly created database and load the 3 files from `setup/MonetDB/` in ascending order

4. You've successfully loaded in the data :D

Install pymonetdb
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

## Run queries
1. run `python analyzeData.py {test_system} {DBMS} {scale_factor}` from the `queries/` directory. This will create 22 result files in `results/{system}/{DBMS}/SF-{scale_factor}/`