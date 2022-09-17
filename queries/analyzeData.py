import pymonetdb
import pandas as pd

if __name__ == '__main__':
    # set up a connection. arguments below are the defaults
    connection = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", database="mydb")

    # create a cursor
    cursor = connection.cursor()

    # increase the rows fetched to increase performance (optional)
    cursor.arraysize = 100

    scale_factor = 1
    query_id = 1

    for file_name in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']:
        with open('MonetDB/q%s.sql' % file_name) as file_object:
            queries = file_object.read().split(';') # skipping the first lines as those are comments
            for query in queries: # every ; indicates a new query
                if query != '\n':
                    cursor.execute(query + ';')
                    try:
                        results = cursor.fetchall()
                        if len(results) > 0:
                            pd.DataFrame(results, columns=[i[0] for i in cursor.description]).to_csv('../results/Job_Desktop/MonetDB/SF-%d/q%d.out' % (scale_factor, query_id), sep='|', index=False)
                    except pymonetdb.exceptions.ProgrammingError:
                        continue
        query_id += 1
