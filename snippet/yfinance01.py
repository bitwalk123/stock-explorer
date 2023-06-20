# Reference:
# https://toukei-lab.com/python_stock

import datetime as dt
import yfinance as yf

start = dt.date(2010, 1, 1)
end = dt.date.today()

# ターゲットを指定
ticker = '4755.T'

# データを収集
#df = yf.download(ticker, period='7d', interval='1d')
df = yf.download(ticker, start, end)
print(df)
