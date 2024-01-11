import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
)

from ui.browser import NewsGoodBad
from ui.sub_good_bad import SubGoodBad


def on_goodbad_requested(dict_df: dict):
    print(dict_df)


def main(url_init: QUrl, script_extract: str):
    app = QApplication()
    ex = NewsGoodBad(url_init, script_extract)
    ex.goodbadRequested.connect(on_goodbad_requested)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url = QUrl('https://selection.kabutan.jp/category/koaku/')
    script = "document.getElementsByClassName('body')[0].innerHTML"
    main(url, script)
