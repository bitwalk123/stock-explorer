import os
import pickle

from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import (
    select_13sector_from_ticker,
    select_13sector_from_ticker_with_code,
)
from database.sqls_trade import select_close_from_trade_with_id_code_date
from functions.get_dict_code import get_dict_code_id_code
from functions.resources import get_connection
from structs.sector_delta import SectorDelta


def diff_close_by_sector(pair_date) -> SectorDelta:
    pkl_sd = 'pool/sd_%d.pkl' % pair_date[1]
    if os.path.isfile(pkl_sd):
        with open(pkl_sd, 'rb') as f:
            sd: SectorDelta = pickle.load(f)
        return sd

    dict_sector_dist = dict()
    dict_sector_price = dict()
    con = get_connection()
    if con.open():
        # dictionary for id_code with key of code
        dict_id_code = get_dict_code_id_code()
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Initialize dictionary for 33業種区分
        set_13sector = set()
        sql = select_13sector_from_ticker()
        query = QSqlQuery(sql)
        while query.next():
            set_13sector.add(query.value(0))
        list_13sector = list(sorted(set_13sector))
        for sector in list_13sector:
            dict_sector_dist[sector] = list()
            dict_sector_price[sector] = list()
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Loop by code
        for code in dict_id_code.keys():
            # _________________________________________________________________
            # 33業種区分
            name_13sector = ''
            sql = select_13sector_from_ticker_with_code(code)
            query = QSqlQuery(sql)
            if query.next():
                name_13sector = query.value(0)
            # _________________________________________________________________
            # day 1
            sql = select_close_from_trade_with_id_code_date(
                dict_id_code[code], pair_date[0]
            )
            query = QSqlQuery(sql)
            if query.next():
                close_1 = query.value(0)
            else:
                continue
            # _________________________________________________________________
            # day 2
            sql = select_close_from_trade_with_id_code_date(
                dict_id_code[code], pair_date[1]
            )
            query = QSqlQuery(sql)
            if query.next():
                close_2 = query.value(0)
            else:
                continue

            diff = close_2 - close_1
            dict_sector_dist[name_13sector].append(diff)
            pair_price = [close_1, close_2]
            dict_sector_price[name_13sector].append(pair_price)
        con.close()

    sd = SectorDelta(dict_sector_dist, dict_sector_price)
    if not os.path.isdir('pool'):
        os.mkdir('pool')
    with open(pkl_sd, 'wb') as f:
        pickle.dump(sd, f)

    return sd
