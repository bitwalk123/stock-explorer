from PySide6.QtWidgets import QComboBox


class ComboBookmark(QComboBox):
    tickers = {
        '東京エレクトロン': ['8035', True],
        'スクリーン': ['7735', True],
        'アドバンテスト': ['6857', True],
        'レーザーテック': ['6920', True],
        'ディスコ': ['6146', True],
        'TSMC': ['TSM', False],
        'Micron': ['MU', False],
        'Intel': ['INTC', False],
        'Lam Research': ['LRCX', False],
        'Applied Materials': ['AMAT', False],
        'NVIDIA': ['NVDA', False],
        'Microsoft': ['MSFT', False],
        'Apple': ['AAPL', False],
        'Alphabet': ['GOOG', False],
        'Amazon': ['AMZN', False],
        'Meta Platforms': ['META', False],
        'Tesla': ['TSLA', False],
    }

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.addItems(list(self.tickers.keys()))

    def getName(self, idx: int) -> str:
        return list(self.tickers.keys())[idx]

    def getTicker(self, idx: int) -> str:
        key = self.getName(idx)
        return self.tickers[key][0]

    def isJPX(self, idx: int) -> bool:
        key = self.getName(idx)
        return self.tickers[key][1]


class ComboTradeRange(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.addItems(['３ヵ月', '６ヵ月', '１年', '２年', '全て'])
        self.setCurrentText('３ヵ月')
