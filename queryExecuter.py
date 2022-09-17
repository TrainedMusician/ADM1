import numpy as np
import pandas as pd
import pymonetdb
import time
import random


def execute_all_queries(order, save_results, machine_type, dbms, scale_factor):
    timing_results = []
    for file_name in order:
        query_id = int(file_name.lstrip('0'))
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
    # set up a connection. arguments below are the defaults
    connection = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", database="mydb")

    # create a cursor
    cursor = connection.cursor()

    # increase the rows fetched to increase performance (optional)
    cursor.arraysize = 100

    machine_type = 'Job_Desktop'
    dbms = 'MonetDB'
    scale_factor = 1

    reps = 30
    total_results = []

    query_ids = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22']
    # query_ids = ['01', '02', '03']


    for repetition in range(reps):
        random.shuffle(query_ids)
        total_results.extend(execute_all_queries(query_ids, True if repetition == 0 else False, machine_type, dbms, scale_factor))

    np.save('../results/binary_results/%s_%s_SF-%d' % (machine_type, dbms, scale_factor), total_results)