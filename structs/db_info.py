from PySide6.QtSql import QSqlDatabase


class DBInfo:
    con: QSqlDatabase = None

    @classmethod
    def get_connection(cls):
        return cls.con

    @classmethod
    def setInfo(
            cls,
            driver: str,
            host: str,
            db_name: str,
            user: str,
            password: str
    ):
        cls.con = QSqlDatabase.addDatabase(driver)
        cls.con.setHostName(host)
        cls.con.setDatabaseName(db_name)
        cls.con.setUserName(user)
        cls.con.setPassword(password)

    @classmethod
    def setInfoDict(cls, dict_info: dict):
        driver = dict_info['driver']
        host = dict_info['host']
        db_name = dict_info['db_name']
        user = dict_info['user']
        password = dict_info['password']
        cls.setInfo(driver, host, db_name, user, password)
