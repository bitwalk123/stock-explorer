import datetime as dt
import os
import pandas as pd

from functions.get_open_with_code import get_open_with_code

os.chdir('../')
os.getcwd()

code = 1301
today = int(pd.to_datetime(str(dt.date.today())).timestamp())
year = 365 * 24 * 60 * 60
start = today - year
cname, list_x, list_y = get_open_with_code(code, start)
series = pd.Series(data=list_y, index=list_x, name=cname)
print(series)
