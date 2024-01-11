import sys

from PySide6.QtQml import QJSEngine, QJSValue
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QSizePolicy, QVBoxLayout


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('テスト')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton(self)
        btn.setText('開　始')
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    def button_clicked(self):
        filename = 'contents.html'
        with open(filename) as f:
            contents = f.read()
        jsEngine = QJSEngine()
        jscript = "element.getElementsByTagName('td');"
        result: QJSValue = jsEngine.evaluate(contents, jscript)
        print(result.property("length").toInt())



def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
