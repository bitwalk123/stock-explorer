from PySide6.QtWidgets import QMessageBox, QFileDialog

from structs.res import AppRes


class DialogWarning(QMessageBox):
    def __init__(self, msg: str):
        super().__init__()
        self.setWindowTitle('警告')
        self.setText(msg)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Warning)


class DialogError(QMessageBox):
    def __init__(self, msg: str):
        super().__init__()
        self.setWindowTitle('エラー')
        self.setText(msg)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Critical)


class FileDialogExcel(QFileDialog):
    def __init__(self, res: AppRes):
        super().__init__()
        # 初期ディレクトリを指定
        self.setDirectory(res.dir_excel)
        # 拡張子のフィルターを設定
        self.setNameFilters(
            [
                'Excel Macro (*.xlsm)',
                'All files (*)',
            ]
        )
