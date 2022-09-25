import pandas as pd
import os


def convert_to_out(scale_factor, query_id):
    query_id_string = query_id
    if query_id < 10:
        query_id_string = '0%d' % query_id
    old_file = os.path.join('answers', 'SF-%d' % scale_factor, 'q%s.res.csv' % query_id_string)
    new_file = os.path.join('answers', 'SF-%d' % scale_factor, 'q%d.out' % query_id)
    if query_id == 11 and scale_factor == 3:
        return
    return pd.read_csv(old_file, header=None).to_csv(new_file, sep='|', index=False, header=True)


if __name__ == '__main__':
    # Be sure you duplicated q01 and renamed it to q23
    scale_factor = 3
    for i in range(23):
        convert_to_out(scale_factor, i + 1)
