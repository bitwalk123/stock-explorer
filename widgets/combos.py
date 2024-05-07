from PySide6.QtWidgets import QComboBox


class ComboBookmark(QComboBox):
    def __init__(self):
        super().__init__()
        self.tickers = self.getTickerList()
        self.setContentsMargins(0, 0, 0, 0)
        self.addItems(list(self.tickers.keys()))

    def getName(self, idx: int) -> str:
        return list(self.tickers.keys())[idx]

    def getTicker(self, idx: int) -> str:
        key = self.getName(idx)
        return self.tickers[key]

    def getTickerList(self) -> dict:
        return {
            '東京エレクトロン': '8035.T',
            'スクリーン': '7735.T',
            'アドバンテスト': '6857.T',
            'レーザーテック': '6920.T',
            'ディスコ': '6146.T',
        }


class ComboBookmarkAll(ComboBookmark):
    def __init__(self):
        super().__init__()

    def getTicker(self, idx: int) -> str:
        key = self.getName(idx)
        return self.tickers[key][0]

    def getTickerList(self) -> dict:
        return {
            '日経平均株価（日経225）': ['^N225', False],
            '東京エレクトロン': ['8035', True],
            'スクリーン': ['7735', True],
            'アドバンテスト': ['6857', True],
            'レーザーテック': ['6920', True],
            'ディスコ': ['6146', True],
            'ダウ工業株30種平均': ['^DJI', False],
            'ナスダック総合指数': ['^IXIC', False],
            'S&P500': ['^GSPC', False],
            'TSMC': ['TSM', False],
            'Micron': ['MU', False],
            'Intel': ['INTC', False],
            'Lam Research': ['LRCX', False],
            'Applied Materials': ['AMAT', False],
            'ASML Holding N.V.': ['ASML', False],
            'ARM Holdings PLC': ['ARM', False],
            'NVIDIA': ['NVDA', False],
            'Microsoft': ['MSFT', False],
            'Apple': ['AAPL', False],
            'Alphabet': ['GOOG', False],
            'Amazon': ['AMZN', False],
            'Meta Platforms': ['META', False],
            'Tesla': ['TSLA', False],
        }

    def isJPX(self, idx: int) -> bool:
        key = self.getName(idx)
        return self.tickers[key][1]


class ComboTradeRange(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.addItems(['３ヵ月', '６ヵ月', '１年', '２年', '全て'])
        self.setCurrentText('３ヵ月')
