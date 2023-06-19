# Reference:
# https://datatechlog.com/how-to-retrieve-stock-price-and-other-info-using-yfinance/
import yfinance as yf

# ソフトバンクグループの情報を取得（Tは東証を表す）
ticker_info = yf.Ticker("9984.T")

# 会社概要(info)を出力
ticker_info.info