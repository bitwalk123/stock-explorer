from PySide6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QTextEdit,
)


class WinHTML(QMainWindow):
    def __init__(self, content: str):
        super().__init__()
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        view = QTextEdit()
        view.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        view.setPlainText(content)
        self.setCentralWidget(view)

        self.resize(1000, 800)
