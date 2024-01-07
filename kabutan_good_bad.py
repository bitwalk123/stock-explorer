import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
)

from ui.browser import NewsGoodBad


def main(url_init: QUrl, script_extract: str):
    app = QApplication()
    ex = NewsGoodBad(url_init, script_extract)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url = QUrl('https://selection.kabutan.jp/category/koaku/')
    script = "document.getElementsByClassName('body')[0].innerHTML"
    main(url, script)
