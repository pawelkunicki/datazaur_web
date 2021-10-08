import investpy
import pandas as pd
import os
from utils.compare_timestamps import compare_timestamps

def econ_calendar():
    file = 'calendar.csv'
    refresh_rate = 86400

    if file not in os.listdir() or not compare_timestamps(refresh_rate, file):
        calendar = investpy.economic_calendar()
        calendar.to_csv(file)
    else:
        calendar = pd.read_csv(file, index_col=0)
    return calendar


