# ADM1

## Setup

### MonetDB (Ubuntu)
1. Install [MonetDB](https://www.monetdb.org/easy-setup/) on your system and create a database
2. Copy the data directory to the `/data/` on your system. Or edit the *absolute* paths in `setup/MonetDB/1-load_data.sql`
3. Create a new database called `ADM`
4. Connect to your newly created database and load the 4 files from `setup/MonetDB/` in ascending order
5. You've successfully loaded in the data :D

### MySQL (Ubuntu)
1. Follow the steps mentioned [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)
2. Copy the data directory to the `/var/lib/mysql-files` on your system.
3. Create a new database called `ADM`
4. Connect to your newly created database and load the 4 files from `setup/MySQL/` in ascending order
5. You've successfully loaded in the data :D


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
1. Lines 104 to 115 contain the connection and machine settings which can be changed before running the script 
2. run `python queryExecuter.py` from the main directory. This will create 23 result files in `results/{system}/{DBMS}/SF-{scale_factor}/`
    There are 22 valid queries which will be checked, the 23rd is a dummy query to ensure that the validating process works.
3. A plot will appear, and when invalid results will return the plot title notify you.

### Convert answer files
If answer files need to be converted from a csv format to .out format with `|` delimiters, change the value at line 18 of `convertAnswerFiles.py` and execute the script


## Dashboard
To open and explore the dashboard, the following packages are required:
- plotly
- pandas
- numpy
- dash
- dash-daq
- dash-bootstrap-components

These packages can be installed with the command `pip install pandas numpy dash dash-daq dash-bootstrap-components`
After installing the packages, simply run `dashboard.py` and open the returned link in any web-browser.



## Custom Implementations
As mentioned in the report, the best performance is when using column names during the loading data step.
`customQ1Implementation.py` and `customQ6Implementation.py` expect the file `data/lineitem.tbl` to be present and will create a modified tmp file which is deleted immedeatly after loading the data.
Simply run both scripts and it will print the runtimes for each part *if* the results are as expected.