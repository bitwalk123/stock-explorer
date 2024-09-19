import sys

from PySide6.QtWidgets import QApplication

from ui.main_trade_day_analysis import MainTradeDayAnalysis


def main():
    app = QApplication(sys.argv)
    win = MainTradeDayAnalysis()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
