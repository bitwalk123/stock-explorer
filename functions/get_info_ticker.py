import os
import pickle

import yfinance as yf


def get_info_ticker(code) -> dict:
    ticker = '%s.T' % code
    dict_info_ticker = None
    pkl_dict_info_ticker = 'pool/dict_info_%s.pkl' % ticker
    if os.path.isfile(pkl_dict_info_ticker):
        with open(pkl_dict_info_ticker, 'rb') as f:
            dict_info_ticker = pickle.load(f)
    else:
        ticker_info = yf.Ticker(ticker)
        dict_info_ticker = ticker_info.info
        with open(pkl_dict_info_ticker, 'wb') as f:
            pickle.dump(dict_info_ticker, f)

    return dict_info_ticker


def get_info_ticker_renew(code) -> dict:
    ticker = '%s.T' % code
    pkl_dict_info_ticker = 'pool/dict_info_%s.pkl' % ticker
    ticker_info = yf.Ticker(ticker)
    dict_info_ticker = ticker_info.info
    with open(pkl_dict_info_ticker, 'wb') as f:
        pickle.dump(dict_info_ticker, f)

    return dict_info_ticker
