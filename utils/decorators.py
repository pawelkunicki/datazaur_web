import os
import datetime
import pandas as pd
from utils.formatting import color_cell, add_hyperlinks

# decorator that checks if a file with data exists and whether it's recent enough.
# refresh rate specifies (in seconds) how often files should be updated
def load_or_save(filename, refresh_rate):
    def decorator(func):
        def wraps(*args, **kwargs):
            if filename in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(filename) < refresh_rate:
                print('from file')
                return pd.read_csv(filename, index_col=0)
            else:
                print('from func')
                data = func(*args, **kwargs)
                df = pd.DataFrame(data)
                df.to_csv(filename)
                return data
        return wraps
    return decorator



@load_or_save('crypto.csv', 1200)
def prep_crypto_display():
    def decorator(func):
        def wraps(*args, **kwargs):
            data = func(*args, **kwargs)
            for col in data.columns:
                if 'Price' in col or 'Δ' in col or 'vol' in col or 'cap' in col or 'Supply' in col:
                    data[col] = data[col].apply(lambda x: format(x, ','))
                    if 'Δ' in col:
                        data[col] = data[col].apply(color_cell)
            data = add_hyperlinks(data)
            if 'Url' in data.columns:
                data.drop('Url', inplace=True, axis=1)
            return data
        return wraps
    return decorator


