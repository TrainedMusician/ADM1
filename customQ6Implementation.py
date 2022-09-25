from datetime import datetime, timedelta
import pandas as pd
import os
from time import time


def load_data(file_name):
    """This function simply loads the lineitem file, it uses the modified file
    which offers a speed boost by only loading the 6 columns
    Returns a pandas DataFrame"""
    columns = ['l_shipdate', 'l_extendedprice', 'l_discount', 'l_quantity']
    tmp = pd.read_csv(file_name, sep="|", skipinitialspace=True,
                      usecols=columns)
    mask = (pd.DatetimeIndex(tmp['l_shipdate']) >= datetime.strptime('1994-01-01', '%Y-%m-%d')) & \
        (pd.DatetimeIndex(tmp['l_shipdate']) < datetime.strptime('1994-01-01', '%Y-%m-%d') + timedelta(days=365.2425)) & \
        (tmp['l_discount'].between(0.059, 0.061)) & (tmp['l_quantity'] < 24)
    return tmp[mask]


def process_data(df):
    """This function calculates the aggregation"""
    e = df['l_extendedprice']
    d = df['l_discount']
    return (e * d).sum()


if __name__ == '__main__':
    query_id = 6
    old_file = os.path.join('data', 'lineitem.tbl')
    new_file = os.path.join('data', 'jobbert.tbl')
    verification_script = os.path.join('answers', 'cmpq.pl')
    correct_output = os.path.join('answers', 'query_outputs',
                                  'q%d.out' % query_id)
    tmp_file = os.path.join('results', 'customQ6tmp.txt')
    comparison_file = os.path.join('results', 'comparison_tmp.txt')

    print('Adding the columns..')
    data_preparation = time()
    os.system('bash addColumns.sh %s %s' % (old_file, new_file))
    # using sed would be faster! But not guaranteed to work on all systems...
    data_preparation = time() - data_preparation

    print('Loading data..', end='\t\t')
    data_loading = time()
    data = load_data(new_file)
    os.remove(new_file)  # remove file after loading it in memory
    data_loading = time() - data_loading

    print('Done!\nProcessing data..')
    data_processing = time()
    with open(tmp_file, 'w') as file_object:
        file_object.write('revenue\n')
        file_object.write(str((data['l_extendedprice'] * data['l_discount']).sum()))
    # print(data.apply(process_data, axis=1))
    # df = pd.DataFrame(data.size())
    # df['sum_qty'], df['sum_base_price'], df['sum_disc_price'], df[
    #     'sum_charge'], df['avg_qty'], df['avg_price'], df['avg_disc'], df[
    #     'count_order'] = zip(*grouped_by.apply(process_data))
    # data_processing = time() - data_processing
    #
    # df[['sum_qty', 'sum_base_price', 'sum_disc_price', 'sum_charge',
    #         'avg_qty', 'avg_price', 'avg_disc',
    #         'count_order']].to_csv(tmp_file, sep='|', index=True)
    print('Result is saved in %s, verifying it' % tmp_file)

    data_verification = time()
    os.system('%s %d %s %s > %s' % (
        verification_script, query_id, correct_output, tmp_file, comparison_file))
    data_verification = time() - data_verification

    with open(comparison_file) as file_object:
        if file_object.read() == 'Query 1 0 unacceptable missmatches\n':
            print('Successfully executed query \t%d' % query_id)
            print('Data preparation time:\t\t\t%.5f seconds' % data_preparation)
            print('Data loading time:\t\t\t\t%.5f seconds' % data_loading)
            print('Data processing time:\t\t\t%.5f seconds' % data_processing)
            print('Data verification time:\t\t\t%.5f seconds' % data_verification)
        else:
            print('There is something going wrong, I have wrong results...')
