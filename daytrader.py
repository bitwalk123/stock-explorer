import logging
import os
import re
import sys
import time

if sys.platform == "win32":
    import xlwings as xw
    from pywintypes import com_error  # Windows 固有のライブラリ

    debug = False
else:
    debug = True

from PySide6.QtCore import (
    QDate,
    QDateTime,
    QThread,
    QTime,
    QTimer,
)
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QWidget,
)

from funcs.log import setup_logging
from funcs.tide import get_datetime_today, get_hms, get_yyyy_mm_dd
from structs.res import AppRes, YMD
from modules.trader import TraderUnit, TraderUnitDebug
from widgets.layouts import VBoxLayoutTrader
from widgets.sbars import StatusBarDebug
from widgets.toolbars import ToolBarDayTrader
from modules.xlloader import ExcelLoader


class DayTrader(QMainWindow):
    __app_name__ = "DayTrader"
    __version__ = "0.1.0"

    def __init__(self, options: list = None):
        super().__init__()
        global debug

        # __name__ を指定することで、このモジュール固有のロガーを取得
        # これはルートロガーの子として扱われ、ルートロガーのハンドラを継承する
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"{__name__} initialized.")

        # コンソールから起動した際のオプション・チェック
        if len(options) > 0:
            for option in options:
                if option == "debug":
                    debug = True
                    self.logger.info(f"{__name__} is executed as DEBUG mode!")

        self.res = res = AppRes()

        # ウィンドウ・タイトル
        icon = QIcon(os.path.join(res.dir_image, "trading.png"))
        self.setWindowIcon(icon)
        if debug:
            self.setWindowTitle(f"{self.__app_name__} (debug mode)")
        else:
            self.setWindowTitle(self.__app_name__)

        base = QWidget()
        self.setCentralWidget(base)

        layout = VBoxLayoutTrader()
        layout.setSpacing(1)
        base.setLayout(layout)

        # ticker インスタンスを保持するリスト
        self.list_trader = list_trader = list()

        if debug:
            self.logger.info(f"{__name__} is executed as DEBUG mode on Non-Windows platform!")
            self.xl_loader = None
            self.xl_thread = None

            toolbar = ToolBarDayTrader(res)
            toolbar.openClicked.connect(self.on_load_excel)
            self.addToolBar(toolbar)

            self.statusbar = statusbar = StatusBarDebug()
            self.setStatusBar(statusbar)

            for num in range(3):
                row = num + 1
                trader = TraderUnitDebug(row, res)
                layout.addWidget(trader)
                list_trader.append(trader)
        else:
            # Excelシートから xlwings でデータを読み込むときの試行回数
            self.max_retries = 3  # 最大リトライ回数
            self.retry_delay = 0.1  # リトライ間の遅延（秒）

            #######################################################################
            # 情報を取得する Excel ファイル
            name_excel = "daytrader.xlsx"
            wb = xw.Book(name_excel)
            self.sheet = wb.sheets["Sheet1"]

            # 列情報
            self.col_code = 0
            self.col_name = 1
            self.col_date = 2
            self.col_time = 3
            self.col_price = 4
            self.col_lastclose = 5
            # 行情報
            self.num_max = 3
            #
            #######################################################################

            # 日付・時間情報
            self.dict_dt = dict_dt = get_datetime_today()

            for num in range(self.num_max):
                row = num + 1

                # 指定銘柄
                trader = TraderUnit(row, res)
                # チャートのタイトル
                title = self.get_chart_title(row)
                trader.setTitle(title)
                # X軸の範囲
                trader.setTimeRange(dict_dt["start"], dict_dt["end"])
                # 前日の終値の横線
                p_lastclose = self.get_last_close(row)
                trader.addLastCloseLine(p_lastclose)

                layout.addWidget(trader)
                list_trader.append(trader)

            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # タイマー
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            self.timer = timer = QTimer()
            timer.timeout.connect(self.on_update_data)
            timer.setInterval(1000)
            self.timer.start()
            self.logger.info("Data update timer started.")

    def append_chart_data(self, ticker: TraderUnit, y: float):
        dt = QDateTime.currentDateTime()
        if self.dict_dt["start"] <= dt <= self.dict_dt["end_1h"]:
            ticker.appendPoint(dt, y)
        elif self.dict_dt["start_2h"] <= dt <= self.dict_dt["start_ca"]:
            ticker.appendPoint(dt, y)

    def closeEvent(self, event: QCloseEvent):
        self.logger.info(f"{self.__app_name__} stopped and closed.")
        event.accept()

    def get_chart_title(self, row: int) -> str:
        code = self.sheet[row, self.col_code].value
        name = self.sheet[row, self.col_name].value
        title = f"{name} ({code})"
        return title

    def get_last_close(self, row: int) -> float:
        p_lastclose = self.sheet[row, self.col_lastclose].value
        return p_lastclose

    def on_error(self, message: str):
        self.statusbar.showMessage("エラー: Excelファイルの読み込みに失敗しました。", 5000)
        self.statusbar.setText("エラー")
        QMessageBox.critical(self, "エラー", message)
        self.statusbar.setValue(0)  # エラー時はプログレスバーをリセット

    def on_load_excel(self):
        """
        [debug] Excel ファイルの読み込み
        """
        excel_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            self.res.dir_excel,
            "Excel Files (*.xlsx *.xlsm)"
        )
        if excel_path == "":
            return

        # Excel を読み込むスレッド処理
        self.xl_thread = QThread()
        self.xl_loader = ExcelLoader(excel_path)
        self.xl_loader.moveToThread(self.xl_thread)

        # シグナルとスロットの接続
        self.xl_thread.started.connect(self.xl_loader.run)
        self.xl_loader.progressUpdated.connect(self.update_progress)
        self.xl_loader.finishedLoading.connect(self.on_finished_loading)
        self.xl_loader.errorOccurred.connect(self.on_error)
        self.xl_loader.finishedLoading.connect(self.xl_thread.quit)  # 処理完了時にスレッドを終了
        self.xl_loader.errorOccurred.connect(self.xl_thread.quit)  # エラー時にもスレッドを終了
        self.xl_thread.finished.connect(self.xl_thread.deleteLater)  # スレッドオブジェクトの削除

        # スレッドを開始
        self.xl_thread.start()

    def on_finished_loading(self, dict_sheet: dict, ymd: YMD):
        self.statusbar.setValue(100)
        self.statusbar.showMessage("Excelファイルの読み込みが完了しました！", 5000)  # 5秒間表示
        self.statusbar.setText("読み込み完了")

        pattern = re.compile(r"^tick_(.+)$")
        day_target = QDate(ymd.year, ymd.month, ymd.day)
        self.logger.info(f"取引日: {get_yyyy_mm_dd(day_target)}")

        list_tick = list()
        for name_sheet in dict_sheet.keys():
            if name_sheet != "Cover":
                list_tick.append(name_sheet)

        for trader in self.list_trader:
            # データをクリア
            trader.clear()

        for name_tick, trader in zip(list_tick, self.list_trader):
            # self.logger.info(f"ワークシート '{name_tick}'")
            m = pattern.match(name_tick)
            if m:
                code = m.group(1)
            else:
                code = "Unknown"
            trader.setTitle(code)

            # ティックデータのデータフレーム
            df = dict_sheet[name_tick]

            # x軸（時間軸）の範囲（市場の開場時間）
            dt_start = QDateTime(day_target, QTime(9, 0, 0))
            dt_end = QDateTime(day_target, QTime(15, 30, 0))
            trader.setTimeRange(dt_start, dt_end)

            # チャートへデータを一つづつプロット
            for x, y in zip(df['Time'], df['Price']):
                # ログデータの時刻はミリ秒単位のタイムスタンプ
                trader.appendPointTimestamp(x, y)
            QApplication.processEvents()

        self.statusbar.setValue(0)
        self.statusbar.setText("プロット完了")

    def on_update_data(self):
        for ticker in self.list_trader:
            self.read_excel_with_xlwings(ticker)

    def read_excel_with_xlwings(self, ticker: TraderUnit):
        row = ticker.getRow()
        # Excel シートから株価情報を取得
        for attempt in range(self.max_retries):
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # 楽天証券のマーケットスピード２ RSS の書き込みと重なる（衝突する）と、
            # COM エラーが発生するためリトライできるようにしている。
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            try:
                # Excelシートから株価データを取得
                y = self.sheet[row, self.col_price].value
                if y > 0:
                    # y = 0 の時はまだ寄っていない。
                    self.append_chart_data(ticker, y)
                break
            except com_error as e:
                # com_error は Windows 固有
                if attempt < self.max_retries - 1:
                    self.logger.warning(
                        f"COM Error occurred, retrying... (Attempt {attempt + 1}/{self.max_retries}) Error: {e}"
                    )
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error(
                        f"COM Error occurred after {self.max_retries} attempts. Giving up."
                    )
                    raise  # 最終的に失敗したら例外を再発生させる
            except Exception as e:
                self.logger.exception(f"An unexpected error occurred: {e}")
                raise  # その他の例外はそのまま発生させる
        # ... (読み込んだ株価を使ったトレンドチャート作成の処理) ...

    def update_progress(self, name_sheet, sheet_num, total_sheets):
        progress = int((sheet_num / total_sheets) * 100)
        self.statusbar.setValue(progress)
        self.statusbar.setText(
            f"読み込み中: シート '{name_sheet}' ({sheet_num}/{total_sheets})"
        )


def main():
    app = QApplication(sys.argv)
    options = sys.argv[1:]
    win = DayTrader(options)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # ロギング設定を適用（ルートロガーを設定）
    main_logger = setup_logging()
    # main_logger.info("Application starting up and logging initialized.")
    main()
