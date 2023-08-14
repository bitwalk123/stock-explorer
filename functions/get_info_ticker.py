import yfinance as yf


def get_info_ticker(code) -> dict:
    ticker = '%s.T' % code
    ticker_info = yf.Ticker(ticker)
    return ticker_info.info
