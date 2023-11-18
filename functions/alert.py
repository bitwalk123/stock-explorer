from widgets.dialog import DialogAlert


def alert_no_ticker(ticker):
    dlg = DialogAlert()
    dlg.setText('There is not ticker, \'%s\'!' % ticker)
    dlg.exec()
