import os
import datetime
import pandas as pd

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

                pd.DataFrame(data).to_csv(filename)
                return data
        return wraps
    return decorator