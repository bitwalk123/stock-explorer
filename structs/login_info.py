from PySide6.QtCore import QUrl


class LoginInfo:
    def __init__(self, login_info: dict):
        self.login_info = login_info

    def getLoginID(self) -> str:
        return self.login_info['loginid']

    def getPassword(self) -> str:
        return self.login_info['password']

    def getURL(self) -> QUrl:
        return QUrl(self.login_info['url'])
