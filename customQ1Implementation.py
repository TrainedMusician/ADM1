import filecmp
import pandas as pd
import os


def load_data(file_name):
    """This function simply loads the lineitem file, it uses the modified file
    which offers a speed boost by only loading the 6 columns
    Returns a pandas DataFrame"""
    columns = ['l_returnflag', 'l_linestatus', 'l_quantity', 'l_extendedprice',
               'l_discount', 'l_tax']
    return pd.read_csv(file_name, sep="|", skipinitialspace=True,
                       usecols=columns)


def process_data(df):
    """This function calculates the 'difficult' two aggregations"""
    e = df['l_extendedprice']
    d = df['l_discount']
    t = df['l_tax']
    return (e * (1 - d)).sum(), (e * (1 - d) * (1 + t)).sum()


if __name__ == '__main__':
    query_id = 1
    old_file = os.path.join('data', 'lineitem.tbl')
    new_file = os.path.join('data', 'jobbert.tbl')
    # output_file = os.path.join('answers', 'analysis_%d.log' % query_id)
    verification_script = os.path.join('answers', 'cmpq.pl')
    correct_output = os.path.join('answers', 'query_outputs',
                                  'q%d.out' % query_id)
    tmp_file = os.path.join('results', 'customQ1tmp.txt')
    comparison_file = os.path.join('results', 'comparison_tmp.txt')

    print('Adding the columns..')
    os.system('bash addColumns.sh %s %s' % (old_file, new_file))
    # using sed would be faster! But not guaranteed to work on all systems...

    print('Loading data..', end='\t\t')
    data = load_data(new_file)
    os.remove(new_file)  # remove file after loading it in memory

    print('Done!\nProcessing data..')
    grouped_by = data.groupby(
        by=['l_returnflag', 'l_linestatus'])
    result = grouped_by.agg(
        sum_qty=('l_quantity', 'sum'),
        sum_base_price=('l_extendedprice', 'sum'),
        avg_qty=('l_quantity', 'mean'),
        avg_price=('l_extendedprice', 'mean'),
        avg_disc=('l_discount', 'mean'),
        count_order=('l_discount', 'size')
    )

    result['sum_disc_price'], result['sum_charge'] = zip(
        *grouped_by.apply(process_data))

    result[['sum_qty', 'sum_base_price', 'sum_disc_price', 'sum_charge',
            'avg_qty', 'avg_price', 'avg_disc',
            'count_order']].to_csv(tmp_file, sep='|', index=True)
    print('Result is saved in %s, verifying it' % tmp_file)

    os.system('%s %d %s %s > %s' % (
        verification_script, query_id, correct_output, tmp_file, comparison_file))

    with open(comparison_file) as file_object:
        print(file_object.read())
        print('This is because I still need to add the WHERE filter.. Will do this tomorrow!')
    #     if file_object.read() == 'Query 1 0 unacceptable missmatches':
