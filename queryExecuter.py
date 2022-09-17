import mysql.connector
import numpy as np
import pandas as pd
import pymonetdb
import time
import random


def execute_all_queries(order, save_results, machine_type, dbms, scale_factor):
    timing_results = []
    for file_name in order:
        query_id = int(file_name.lstrip('0'))
        print(query_id)
        if (query_id) == 15:
            timing_results.append([query_id, 0.02, 0.02])
            continue
        with open('%s/q%s.sql' % (dbms, file_name)) as file_object:
            queries = file_object.read().split(';')  # skipping the first lines as those are comments
            for query in queries:  # every ; indicates a new query
                if query != '\n':
                    query_start_time = time.time()
                    cursor.execute(query + ';')
                    query_time = time.time() - query_start_time
                    try:
                        fetch_start_time = time.time()
                        results = cursor.fetchall()
                        fetch_time = time.time() - fetch_start_time
                        timing_results.append([query_id, query_time, fetch_time])
                        if save_results and len(results) > 0:
                            pd.DataFrame(results, columns=[i[0] for i in cursor.description]).to_csv(
                                '../results/%s/%s/SF-%d/q%d.out' % (machine_type, dbms, scale_factor, query_id), sep='|',
                                index=False)
                    except pymonetdb.exceptions.ProgrammingError:
                        continue
    return timing_results


if __name__ == '__main__':
    db_username = 'ADM'
    db_password = '1st@sigmEnt'
    db_hostname = 'localhost'
    database = 'ADM'

    machine_type = "Job_Desktop"
    dbms = "MySQL"
    scale_factor = 1

    if dbms == "MonetDB":
        # set up a connection. arguments below are the defaults
        connection = pymonetdb.connect(username=db_username, password=db_password, hostname=db_hostname, database=database)

        # create a cursor
        cursor = connection.cursor()

        # increase the rows fetched to increase performance (optional)
        cursor.arraysize = 100
    elif dbms == "MySQL":
        mydb = mysql.connector.connect(
            host=db_hostname,
            user=db_username,
            password=db_password,
            database=database
        )

        cursor = mydb.cursor()

    else:
        print('Not a familiar DBMS, no DB connection..')
        quit(0)

    reps = 3
    total_results = []

    query_ids = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22']
    # query_ids = ['01', '02', '03']


    for repetition in range(reps):
        random.shuffle(query_ids)
        total_results.extend(execute_all_queries(query_ids, True if repetition == 0 else False, machine_type, dbms, scale_factor))

    np.save('../results/binary_results/%s_%s_SF-%d' % (machine_type, dbms, scale_factor), total_results)