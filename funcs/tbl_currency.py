from PySide6.QtSql import QSqlQuery

from sqls.sql_currency import (
    sql_create_tbl_currency,
    sql_drop_tbl_currency,
    sql_ins_into_currency_vals,
    sql_sel_id_currency_currency_from_currency,
    sql_sel_id_currency_from_currency_with_currency,
    sql_upd_currency_vals,
)
from structs.db_info import DBInfo

list_currency = [
    ['USDJPY', 'USA dollar (USD)', 'TRUE'],
    ['GBPJPY', 'Great Britain pound (GBP)', 'TRUE'],
    ['INRJPY', 'India rupee (INR)', 'TRUE'],
    ['IDRJPY', 'Indonesia rupiah (IDR)', 'TRUE'],
    ['EGPJPY', 'Egypt pound (EGP)', 'TRUE'],
    ['AUDJPY', 'Australia dollar (AUD)', 'TRUE'],
    ['CADJPY', 'Canada dollar (CAD)', 'TRUE'],
    ['KRWJPY', 'Korea won (KRW)', 'TRUE'],
    ['KWDJPY', 'Kuwait dinar (KWD)', 'FALSE'],
    ['COPJPY', 'Colombia peso (COP)', 'FALSE'],
    ['SARJPY', 'Saudi Arabia riyal (SAR)', 'TRUE'],
    ['SGDJPY', 'Singapore dollar (SGD)', 'TRUE'],
    ['CHFJPY', 'Switzerland franc (CHF)', 'TRUE'],
    ['SEKJPY', 'Sweden krona (SEK)', 'TRUE'],
    ['THBJPY', 'Thai baht (THB)', 'TRUE'],
    ['TWDJPY', 'Taiwan dollar (TWD)', 'TRUE'],
    ['CNYJPY', 'China yuan (CNY)', 'TRUE'],
    ['CLPJPY', 'Chile peso (CLP)', 'FALSE'],
    ['DKKJPY', 'Denmark krone (DKK)', 'TRUE'],
    ['TRYJPY', 'Turkey lira (TRY)', 'TRUE'],
    ['NZDJPY', 'New Zealand dollar (NZD)', 'TRUE'],
    ['NOKJPY', 'Norway krone (NOK)', 'TRUE'],
    ['PYGJPY', 'Paraguay guarani (PYG)', 'FALSE'],
    ['PHPJPY', 'Philippines peso (PHP)', 'TRUE'],
    ['BRLJPY', 'Brazil real (BRL)', 'TRUE'],
    ['VESJPY', 'Venezuela bolívar soberano (VES)', 'FALSE'],
    ['PENJPY', 'Peru Nuevo sol (PEN)', 'FALSE'],
    ['HKDJPY', 'Hong Kong dollar (HKD)', 'TRUE'],
    ['MYRJPY', 'Malaysia ringgit (MYR)', 'TRUE'],
    ['ZARJPY', 'South Africa rand (ZAR)', 'TRUE'],
    ['MXNJPY', 'Mexico peso (MXN)', 'TRUE'],
    ['AEDJPY', 'UAE dirham (AED)', 'TRUE'],
    ['EURJPY', 'EU euro (EUR)', 'TRUE'],
    ['JODJPY', 'Jordan dinar (JOD)', 'FALSE'],
    ['RONJPY', 'Romania leu (RON)', 'FALSE'],
    ['LBPJPY', 'Lebanon dollar (LBP)', 'FALSE'],
    ['RUBJPY', 'Russia ruble (RUB)', 'TRUE'],
]


def create_tbl_currency():
    con = DBInfo.get_connection()

    if con.open():
        print('connected!')
        create_tbl_currency_procs_1()
        create_tbl_currency_procs_2()
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False


def create_tbl_currency_procs_1():
    query = QSqlQuery()
    sql = sql_create_tbl_currency()
    result = query.exec(sql)
    if result:
        print('query has been successfully executed.')


def create_tbl_currency_procs_2():
    query = QSqlQuery()
    for row in list_currency:
        sql = sql_sel_id_currency_from_currency_with_currency(row[0])
        query.exec(sql)
        if query.next():
            id_currency = query.value(0)
            sql = sql_upd_currency_vals(id_currency, row)
        else:
            sql = sql_ins_into_currency_vals(row)
        result = query.exec(sql)
        if result:
            print('query has been successfully executed.')


def drop_tbl_currency() -> bool:
    con = DBInfo.get_connection()

    if con.open():
        query = QSqlQuery()
        sql = sql_drop_tbl_currency()
        result = query.exec(sql)
        con.close()
        return result
    else:
        print('database can not be opened!')
        return False


def get_dict_currency() -> dict:
    """
    dict_currency[id_currency] = currency
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_currency = dict()
        query = QSqlQuery()
        sql = sql_sel_id_currency_currency_from_currency()
        query.exec(sql)
        while query.next():
            id_currency = query.value(0)
            currency = query.value(1)
            dict_currency[id_currency] = currency
        con.close()
        return dict_currency
    else:
        print('database can not be opened!')
        return dict()


def get_dict_id_currency() -> dict:
    """
    dict_id_currency[currency] = id_currency
    """
    con = DBInfo.get_connection()
    if con.open():
        dict_id_currency = dict()
        query = QSqlQuery()
        sql = sql_sel_id_currency_currency_from_currency()
        query.exec(sql)
        while query.next():
            id_currency = query.value(0)
            currency = query.value(1)
            dict_id_currency[currency] = id_currency
        con.close()
        return dict_id_currency
    else:
        print('database can not be opened!')
        return dict()
