from datetime import datetime, timedelta
import pandas as pd
import os
from time import time


def load_data(file_name):
    """This function simply loads the lineitem file, it uses the modified file
    which offers a speed boost by only loading the 6 columns
    Returns a pandas DataFrame"""
    columns = ['l_shipdate', 'l_returnflag', 'l_linestatus', 'l_quantity',
               'l_extendedprice', 'l_discount', 'l_tax']
    tmp = pd.read_csv(file_name, sep="|", skipinitialspace=True, usecols=columns)
    return tmp[pd.DatetimeIndex(tmp['l_shipdate']) <= datetime.strptime('1998-12-01', '%Y-%m-%d') - timedelta(days=90)]


def process_data(df):
    """This function calculates the aggregations,
    including the 'difficult' ones"""
    e = df['l_extendedprice']
    d = df['l_discount']
    t = df['l_tax']
    q = df['l_quantity']
    return q.sum(), e.sum(), (e * (1 - d)).sum(), \
           (e * (1 - d) * (1 + t)).sum(), q.mean(), e.mean(), d.mean(), \
           q.size


if __name__ == '__main__':
    query_id = 1
    scale_factor = 1
    old_file = os.path.join('data', 'lineitem.tbl')
    new_file = os.path.join('data', 'jobbert.tbl')
    verification_script = os.path.join('answers', 'cmpq.pl')
    correct_output = os.path.join('answers', 'SF-%d' % scale_factor,
                                  'q%d.out' % query_id)
    tmp_file = os.path.join('results', 'customQ1tmp.txt')
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
    grouped_by = data.groupby(
        by=['l_returnflag', 'l_linestatus'])
    # result = grouped_by.agg(
    #     sum_qty=('l_quantity', 'sum'),
    #     sum_base_price=('l_extendedprice', 'sum'),
    #     avg_qty=('l_quantity', 'mean'),
    #     avg_price=('l_extendedprice', 'mean'),
    #     avg_disc=('l_discount', 'mean'),
    #     count_order=('l_discount', 'size')
    # )
    #
    df = pd.DataFrame(grouped_by.size())
    df['sum_qty'], df['sum_base_price'], df['sum_disc_price'], df[
        'sum_charge'], df['avg_qty'], df['avg_price'], df['avg_disc'], df[
        'count_order'] = zip(*grouped_by.apply(process_data))
    data_processing = time() - data_processing

    df[['sum_qty', 'sum_base_price', 'sum_disc_price', 'sum_charge',
            'avg_qty', 'avg_price', 'avg_disc',
            'count_order']].to_csv(tmp_file, sep='|', index=True)
    print('Result is saved in %s, verifying it' % tmp_file)

    data_verification = time()
    os.system('%s %d %s %s > %s' % (
        verification_script, query_id, correct_output, tmp_file, comparison_file))
    data_verification = time() - data_verification

    # with open(comparison_file) as file_object:
        # if file_object.read() == 'Query 1 0 unacceptable missmatches\n':
    print('Successfully executed query \t%d' % query_id)
    print('Data preparation time:\t\t\t%.5f seconds' % data_preparation)
    print('Data loading time:\t\t\t\t%.5f seconds' % data_loading)
    print('Data processing time:\t\t\t%.5f seconds' % data_processing)
    print('Data verification time:\t\t\t%.5f seconds' % data_verification)
        # else:
        #     print('There is something going wrong, I have wrong results...')
