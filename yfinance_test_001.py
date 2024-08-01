import datetime as dt
import yfinance as yf

if __name__ == '__main__':
    yf.set_tz_cache_location('Asia/Tokyo')
    ticker = yf.Ticker('USDJPY=X')
    end = dt.date.today()
    delta = dt.timedelta(days=1)
    start = end - delta

    df = ticker.history(start=start, end=end, interval='1m')
    print(df)
