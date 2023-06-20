# Reference:
# https://datatechlog.com/how-to-retrieve-stock-price-and-other-info-using-yfinance/
# import datetime
import datetime as dt

import pandas_datareader.data as web

# start = datetime.date(2010, 1, 1)
# end = datetime.date.today()
start = dt.date(2019, 1, 1)
end = dt.date(2020, 1, 1)

df = web.DataReader('9984.T', 'yahoo', start, end)
# df = web.DataReader('9432.T', "yahoo", start, end)
# symbol = 'WIKI/AAPL'  # or 'AAPL.US'
# df = web.DataReader(symbol, 'quandl', '2015-01-01', '2015-01-05')
# df = web.DataReader('GE', 'yahoo', start='2019-09-10', end='2019-10-09')
# df = web.DataReader('GOOG', 'yahoo-actions', start, end)
print(df)
