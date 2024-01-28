from PySide6.QtCore import QUrl


class AppRes:
    tse = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

    path_image = 'images'

    kabutan_koaku = QUrl('https://selection.kabutan.jp/category/koaku/')
    jscrupt_body0_inner_html = "document.getElementsByClassName('body')[0].innerHTML"

    rakuten = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')
    jscript_oneday_ranking = "document.getElementById('margin-oneday-ranking').innerHTML"

    candle_style = 'binance'

    def getCandleStyle(self) -> str:
        return self.candle_style

    def getImagePath(self) -> str:
        return self.path_image

    def getJScriptBody0(self) -> str:
        return self.jscrupt_body0_inner_html

    def getJScriptOneDayRanking(self) -> str:
        return self.jscript_oneday_ranking

    def getURLKabutanKoaku(self) -> QUrl:
        return self.kabutan_koaku

    def getURLRakuten(self) -> QUrl:
        return self.rakuten

    def getTSE(self) -> str:
        return self.tse
