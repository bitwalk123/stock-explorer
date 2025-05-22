import logging
import os
import sys
import time

from funcs.log import setup_logging
from widgets.pbar import ProgressBar
from widgets.toolbar import ToolBarDayTrader
from worker.xlloader import ExcelLoader

if sys.platform == 'win32':
    import xlwings as xw
    from pywintypes import com_error  # Windows 固有のライブラリ

    debug = False
else:
    debug = True

from PySide6.QtCore import (
    QDateTime,
    QThread,
    QTimer,
    Qt,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QStatusBar,
    QWidget,
)

from funcs.tide import get_datetime_today
from structs.res import AppRes
from widgets.container import WidgetTicker, WidgetTickerDebug
from widgets.layout import VBoxLayout


class DayTrader(QMainWindow):
    def __init__(self):
        super().__init__()
        # __name__ を指定することで、このモジュール固有のロガーを取得
        # これはルートロガーの子として扱われ、ルートロガーのハンドラを継承する
        self.logger = logging.getLogger(__name__)
        self.logger.info('MyApp initialized.')  # これがログ出力されるようになる

        self.res = res = AppRes()

        # ウィンドウ・タイトル
        icon = QIcon(os.path.join(res.dir_image, 'trading.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('DayTrader')

        base = QWidget()
        self.setCentralWidget(base)

        layout = VBoxLayout()
        base.setLayout(layout)

        # ticker インスタンスを保持するリスト
        self.list_ticker = list_ticker = list()

        if debug:
            self.excel_loader = None
            self.excel_thread = None

            toolbar = ToolBarDayTrader(res)
            toolbar.fileSelected.connect(self.on_load_excel)
            self.addToolBar(toolbar)

            self.statusbar = statusbar = QStatusBar()
            self.setStatusBar(statusbar)
            self.pbar = pbar = ProgressBar()
            statusbar.addPermanentWidget(pbar)  # 永続的に表示
            self.lab_status = lab_status = QLabel('準備完了')
            statusbar.addWidget(lab_status)

            for num in range(3):
                row = num + 1
                ticker = WidgetTickerDebug(row, res)
                layout.addWidget(ticker)
                list_ticker.append(ticker)
        else:
            # Excelシートから xlwings でデータを読み込むときの試行回数
            self.max_retries = 3  # 最大リトライ回数
            self.retry_delay = 0.1  # リトライ間の遅延（秒）

            #######################################################################
            # 情報を取得する Excel ファイル
            name_excel = 'daytrader.xlsx'
            wb = xw.Book(name_excel)
            self.sheet = wb.sheets['Sheet1']

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
                ticker = WidgetTicker(row, res)
                # チャートのタイトル
                title = self.get_chart_title(row)
                ticker.setTitle(title)
                # X軸の範囲
                ticker.setTimeRange(dict_dt['start'], dict_dt['end'])
                # 前日の終値の横線
                p_lastclose = self.get_last_close(row)
                ticker.addLastCloseLine(p_lastclose)

                layout.addWidget(ticker)
                list_ticker.append(ticker)

            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # タイマー
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            self.timer = timer = QTimer()
            timer.timeout.connect(self.on_update_data)
            timer.setInterval(1000)
            self.timer.start()
            self.logger.info('Data update timer started.')

    def append_chart_data(self, ticker: WidgetTicker, y: float):
        dt = QDateTime.currentDateTime()
        if self.dict_dt['start'] <= dt <= self.dict_dt['end_1h']:
            ticker.appendPoint(dt, y)
        elif self.dict_dt['start_2h'] <= dt <= self.dict_dt['start_ca']:
            ticker.appendPoint(dt, y)

    def get_chart_title(self, row: int) -> str:
        code = self.sheet[row, self.col_code].value
        name = self.sheet[row, self.col_name].value
        title = '%s (%s)' % (name, code)
        return title

    def get_last_close(self, row: int) -> float:
        p_lastclose = self.sheet[row, self.col_lastclose].value
        return p_lastclose

    def on_error(self, message: str):
        self.statusbar.showMessage("エラー: Excelファイルの読み込みに失敗しました。", 5000)
        self.lab_status.setText("エラー")
        QMessageBox.critical(self, "エラー", message)
        self.pbar.setValue(0)  # エラー時はプログレスバーをリセット

    def on_load_excel(self, excel_path: str):
        """
        [debug] Excel ファイルの読み込み
        :return:
        """
        self.excel_thread = QThread()
        self.excel_loader = ExcelLoader(excel_path)
        self.excel_loader.moveToThread(self.excel_thread)

        # シグナルとスロットの接続
        self.excel_thread.started.connect(self.excel_loader.run)
        self.excel_loader.progressUpdated.connect(self.update_progress)
        self.excel_loader.finishedLoading.connect(self.on_finished_loading)
        self.excel_loader.errorOccurred.connect(self.on_error)
        self.excel_loader.finishedLoading.connect(self.excel_thread.quit)  # 処理完了時にスレッドを終了
        self.excel_loader.errorOccurred.connect(self.excel_thread.quit)  # エラー時にもスレッドを終了
        self.excel_thread.finished.connect(self.excel_thread.deleteLater)  # スレッドオブジェクトの削除

        # スレッドを開始
        self.excel_thread.start()

    def on_finished_loading(self, dict_sheet: dict):
        self.pbar.setValue(100)
        self.statusbar.showMessage("Excelファイルの読み込みが完了しました！", 5000)  # 5秒間表示
        self.lab_status.setText("読み込み完了")

        # 読み込んだデータの中身をターミナルに表示 (デバッグ用)
        QMessageBox.information(
            self, "読み込み完了",
            "Excelファイルの読み込みが完了しました。\n詳細をコンソールに出力します。"
        )
        for sheet_name, df in dict_sheet.items():
            print(f"\n--- ワークシート: {sheet_name} ---")
            print(df.head())  # 各データフレームの先頭5行を表示
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")

    def on_update_data(self):
        for ticker in self.list_ticker:
            self.read_excel_with_xlwings(ticker)

    def read_excel_with_xlwings(self, ticker: WidgetTicker):
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
                        f"COM Error occurred, retrying... (Attempt {attempt + 1}/{self.max_retries})"
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
        self.pbar.setValue(progress)
        self.lab_status.setText(
            f"読み込み中: シート '{name_sheet}' ({sheet_num}/{total_sheets})"
        )


def main():
    app = QApplication(sys.argv)
    ex = DayTrader()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # ロギング設定を適用（ルートロガーを設定）
    main_logger = setup_logging()
    # main_logger.info("Application starting up and logging initialized.")
    main()
