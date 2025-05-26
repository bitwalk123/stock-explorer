import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QToolButton,
    QStatusBar, QProgressBar, QFileDialog, QMessageBox,
    QStyle, QLabel
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import (
    Qt, QThread, Signal, QObject
)
import openpyxl
import os


class ExcelLoader(QObject):
    # 進捗更新用のシグナル (現在のワークシート名, 現在のワークシート番号, 総ワークシート数)
    progress_updated = Signal(str, int, int)
    # 読み込み完了シグナル (読み込んだデータフレームの辞書)
    loading_finished = Signal(dict)
    # エラーシグナル
    error_occurred = Signal(str)

    def __init__(self, excel_path):
        super().__init__()
        self.excel_path = excel_path

    def run(self):
        try:
            workbook = openpyxl.load_workbook(self.excel_path)
            excel_data = {}
            total_sheets = len(workbook.sheetnames)

            for i, sheet_name in enumerate(workbook.sheetnames):
                # QThread.isInterruptionRequested() をチェックして、スレッド停止要求に対応
                if QThread.currentThread().isInterruptionRequested():
                    self.error_occurred.emit("Excelファイルの読み込みが中断されました。")
                    return

                self.progress_updated.emit(sheet_name, i + 1, total_sheets)
                sheet = workbook[sheet_name]
                data = sheet.values
                columns = next(data, None)
                if columns:
                    df = pd.DataFrame(data, columns=columns)
                else:
                    df = pd.DataFrame(data)

                excel_data[sheet_name] = df

            workbook.close()
            self.loading_finished.emit(excel_data)

        except Exception as e:
            self.error_occurred.emit(f"Excelファイルの読み込み中にエラーが発生しました: {e}\n"
                                     "'.xls'ファイルの場合、xlrdライブラリが不足しているか、\n"
                                     "openpyxlが対応していない可能性があります。")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excelファイルローダー (PySide6)")
        self.setGeometry(100, 100, 800, 600)

        self.excel_data_dict = {}  # 読み込んだExcelデータを保存する辞書
        self.excel_thread = None  # QThreadインスタンスの参照を保持
        self.excel_loader = None  # ExcelLoaderインスタンスの参照を保持

        self._create_toolbar()
        self._create_statusbar()

    def _create_toolbar(self):
        toolbar = QToolBar("ツールバー")
        self.addToolBar(toolbar)

        open_action = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon), "Excelファイルを開く", self)
        open_action.triggered.connect(self._open_excel_file)
        toolbar.addAction(open_action)

    def _create_statusbar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.statusBar.addPermanentWidget(self.progressBar)

        self.status_message_label = QLabel("準備完了", self)
        self.statusBar.addWidget(self.status_message_label)

    def _open_excel_file(self):
        # 既にスレッドが実行中の場合は、中断を試みる（任意）
        if self.excel_thread and self.excel_thread.isRunning():
            reply = QMessageBox.question(self, "処理中",
                                         "現在、Excelファイルを読み込み中です。\n"
                                         "新しいファイルを読み込むために現在の処理を中断しますか？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.excel_thread.requestInterruption()  # 中断要求
                self.excel_thread.quit()
                self.excel_thread.wait(5000)  # 最大5秒待機
                if self.excel_thread.isRunning():  # 強制終了が必要な場合 (通常は避けるべき)
                    self.excel_thread.terminate()
                    self.excel_thread.wait()

                # 古いオブジェクトへの参照をクリア
                self.excel_thread = None
                self.excel_loader = None
            else:
                return  # ユーザーが中断しないことを選択したら処理を中止

        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls *.xlsm);;All Files (*)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                excel_path = selected_files[0]
                self.statusBar.showMessage(f"選択されたファイル: {os.path.basename(excel_path)}")
                self.progressBar.setValue(0)
                self.status_message_label.setText("読み込み中...")
                self._load_excel_in_thread(excel_path)

    def _load_excel_in_thread(self, excel_path):
        # 毎回新しいQThreadとExcelLoaderインスタンスを作成
        self.excel_thread = QThread(self)  # 親を指定することで、親が削除されたときに一緒に削除される
        self.excel_loader = ExcelLoader(excel_path)
        self.excel_loader.moveToThread(self.excel_thread)

        # シグナルとスロットの接続
        self.excel_thread.started.connect(self.excel_loader.run)
        self.excel_loader.progress_updated.connect(self._update_progress_bar)
        self.excel_loader.loading_finished.connect(self._on_loading_finished)
        self.excel_loader.error_occurred.connect(self._on_error_occurred)

        # 処理完了またはエラー時にスレッドを終了させ、関連オブジェクトを削除
        self.excel_loader.loading_finished.connect(self.excel_thread.quit)
        self.excel_loader.error_occurred.connect(self.excel_thread.quit)

        # スレッド終了時にexcel_loader (ワーカー) とスレッド自身を削除
        self.excel_thread.finished.connect(self.excel_loader.deleteLater)
        self.excel_thread.finished.connect(self.excel_thread.deleteLater)

        # スレッド開始
        self.excel_thread.start()

    def _update_progress_bar(self, sheet_name, current_sheet_num, total_sheets):
        progress_percentage = int((current_sheet_num / total_sheets) * 100)
        self.progressBar.setValue(progress_percentage)
        self.status_message_label.setText(f"読み込み中: シート '{sheet_name}' ({current_sheet_num}/{total_sheets})")

    def _on_loading_finished(self, excel_data_dict):
        self.excel_data_dict = excel_data_dict
        self.progressBar.setValue(100)
        self.statusBar.showMessage("Excelファイルの読み込みが完了しました！", 5000)
        self.status_message_label.setText("読み込み完了")

        QMessageBox.information(self, "読み込み完了",
                                "Excelファイルの読み込みが完了しました。\n詳細をコンソールに出力します。")
        for sheet_name, df in self.excel_data_dict.items():
            print(f"\n--- ワークシート: {sheet_name} ---")
            print(df.head())
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")

        # スレッドとローダーオブジェクトへの参照をクリア
        self.excel_thread = None
        self.excel_loader = None

    def _on_error_occurred(self, error_message):
        self.statusBar.showMessage("エラー: Excelファイルの読み込みに失敗しました。", 5000)
        self.status_message_label.setText("エラー")
        QMessageBox.critical(self, "エラー", error_message)
        self.progressBar.setValue(0)

        # スレッドとローダーオブジェクトへの参照をクリア
        self.excel_thread = None
        self.excel_loader = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())