from PySide6.QtCore import QUrl


class AppRes():
    tse = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

    path_image = 'images'

    kabutan_koaku = QUrl('https://selection.kabutan.jp/category/koaku/')
    jscrupt_inner_html = "document.getElementsByClassName('body')[0].innerHTML"

    def getImagePath(self) -> str:
        return self.path_image

    def getURLKabutanKoaku(self) -> QUrl:
        return self.kabutan_koaku

    def getJScriptInnerHTML(self) -> str:
        return self.jscrupt_inner_html

    def getTSE(self) -> str:
        return self.tse
