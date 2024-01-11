import re
import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
)

from ui.browser import RakutenRanking


def on_parse_requested(content: str):
    # いちにち信用ランキング
    pattern_date = r'<p class="pgh-01 align-R">(.+?)更新</p>'
    list_date = re.findall(pattern_date, content, re.DOTALL)
    print(list_date[0])


    pattern_title = r'<h2 id="margin-oneday-ranking-all" class="hdg-l2-01"><span>(.+?)</span></h2>'
    list_title = re.findall(pattern_title, content, re.DOTALL)
    print(list_title[0])

    pattern_header = r'<th class="cell-01 align-C" scope="col">(.+?)</th>\s*<th class="cell-01 align-C" scope="col">(.+?)</th>\s*<th class="cell-01 align-C" scope="col">(.+?)</th>'
    list_header = re.findall(pattern_header, content, re.DOTALL)
    print(list(list_header[0]))

    pattern_content = r'<th class="cell-02 align-C">(\d+?)</th>\s*<td class="align-C">(.+?)</td>\s*<td>(.+?)</td>'
    list_content = re.findall(pattern_content, content, re.DOTALL)
    print(list_content)


def main(url_init: QUrl, script_extract: str):
    app = QApplication()
    ex = RakutenRanking(url_init, script_extract)
    ex.parseRequested.connect(on_parse_requested)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # url = QUrl('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')
    url = QUrl('file:///home/bitwalk/MyProjects/stock-explorer/content.html')
    script = "document.getElementById('margin-oneday-ranking').innerHTML"
    #script = "document.documentElement.innerHTML"
    main(url, script)
