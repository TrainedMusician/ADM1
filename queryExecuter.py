import matplotlib

# Use whatever works for your system
# matplotlib.use('Qt5Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import filecmp
import mysql.connector
import numpy as np
import pandas as pd
import pymonetdb
import time
import random
import os
from Visualizer import time_fetcher, bar_plot


def execute_all_queries(cursor, order, save_results, machine_type, dbms, scale_factor):
    """
    This function iterates through the list of query-file-names (order).
    save_results is a Boolean which determines to save the results, this is only true on the first repetition for performance reasons
    machine_type, dbms and scale_factor are used for file-saving so that we can visualize the data later on
    """
    timing_results = []
    for file_name in order:
        query_id = int(file_name.lstrip('0'))
        if query_id == 15:
            timing_results.append([query_id, 0.02, 0.02])
            continue
        with open('queries/%s/q%s.sql' % (dbms, file_name)) as file_object:
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
                            directory_path = os.path.join('results', machine_type, dbms, 'SF-%d' % scale_factor)
                            if not os.path.exists(directory_path):
                                os.makedirs(directory_path)
                            pd.DataFrame(results, columns=[i[0] for i in cursor.description]).to_csv(
                                os.path.join(directory_path, 'q%d.out' % query_id), sep='|', index=False)
                    except pymonetdb.exceptions.ProgrammingError:
                        continue
    return timing_results


def open_connection(db_username, db_password, db_hostname, database):
    if dbms == "MonetDB":
        # set up a connection. arguments below are the defaults
        connection = pymonetdb.connect(username=db_username, password=db_password, hostname=db_hostname, database=database)

        # create a cursor
        cursor = connection.cursor()

        # increase the rows fetched to increase performance (optional)
        cursor.arraysize = 100
        return cursor
    elif dbms == "MySQL":
        mydb = mysql.connector.connect(
            host=db_hostname,
            user=db_username,
            password=db_password,
            database=database
        )
        return mydb.cursor()
    else:
        print('Not a familiar DBMS, no DB connection..')
        quit(0)

def do_the_work(cursor, repetitions, machine_type, dbms, scale_factor):
    # Don't touch
    total_results = []
    query_ids = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                 '18', '19', '20', '21', '22', '23']

    for repetition in range(reps):
        random.shuffle(query_ids)
        total_results.extend(execute_all_queries(cursor, query_ids, True if repetition == 0 else False, machine_type, dbms, scale_factor))

    np.save(os.path.join('results', 'binary_results', '%s_%s_SF-%d' % (machine_type, dbms, scale_factor)), total_results)


def validate_results(machine_type, dbms, scale_factor):
    # Run the perl script
    os.system('bash %s %s %s %s > %s' % (os.path.join('answers', 'cmpall.sh'), machine_type, dbms, scale_factor, os.path.join('results', 'tmp.txt')))
    files_identical = filecmp.cmp(os.path.join('answers', 'curatedAnswers.txt'), os.path.join('results', 'tmp.txt'))

    if not files_identical:
        # delete the logs, not if the answers are correct
        for i in range(23):
            if os.path.exists('analysis_%d.log' % (i + 1)):
                os.remove('analysis_%d.log' % (i + 1))
    return files_identical


if __name__ == '__main__':
    # Database variables
    db_username = 'ADM'
    db_password = '1st@sigmEnt'
    db_hostname = 'localhost'
    database = 'ADM'

    # Run variables
    machine_type = "Testing_Now"
    dbms = "MonetDB"
    scale_factor = 1
    name_in_plot = "LLLLLeo"
    reps = 30  # preferably 30, but you can decrease this during debugging

    # Create connection
    # cursor = open_connection(db_username, db_password, db_hostname, database)
    #
    # do_the_work(cursor, reps, machine_type, dbms, scale_factor)

    title = 'Results of %s performing on %dGB data with %s' % (dbms, scale_factor, name_in_plot)

    # If results vs answers aren't identical (compared through perl), notify the user
    if not validate_results(machine_type, dbms, scale_factor):
        title += '\nINVALIDATED!! results are not correct'

    bar_plot(title, [time_fetcher(os.path.join('results', 'binary_results', '%s_%s_SF-%d.npy' % (machine_type, dbms, scale_factor)), name_in_plot)],
             'Query',
             'Time (s)',
             True,
             os.path.join('results', 'plot.png'))
