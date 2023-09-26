from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection

con = get_connection()
if con.open():
    sql1 = """
            SELECT date, id_code FROM trade;
    """
    query1 = QSqlQuery(sql1)
    list_date = list()
    list_id_code = list()
    while query1.next():
        list_date.append(query1.value(0))
        list_id_code.append(query1.value(1))

    list_date = sorted(list(set(list_date)))
    list_id_code = sorted(list(set(list_id_code)))
    print(len(list_date), len(list_id_code))

    for date in list_date:
        for id_code in list_id_code:
            sql2 = """
                    SELECT id_trade FROM trade
                    WHERE date=%d AND id_code=%d;
            """ % (date, id_code)
            query2= QSqlQuery(sql2)
            list_id_trade = list()
            while query2.next():
                list_id_trade.append(query2.value(0))
                print(date, id_code, len(list_id_trade))

    con.close()
