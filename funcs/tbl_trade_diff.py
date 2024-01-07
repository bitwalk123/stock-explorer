import os
import pickle
from typing import Union

from PySide6.QtSql import QSqlQuery

from funcs.tbl_ticker import get_dict_id_code
from sqls.sql_ticker import (
    sql_sel_13sector_from_ticker,
    sql_sel_13sector_from_ticker_with_code,
)
from sqls.sql_trade import sql_sel_close_from_trade_with_id_code_date, sql_sel_open_close_from_trade_with_id_code_date
from structs.db_info import DBInfo
from structs.sector_delta import SectorDelta


def diff_close_by_sector(pair_date: list) -> Union[SectorDelta, None]:
    pkl_cd = 'pool/close_diff_%d.pkl' % pair_date[1]
    if os.path.isfile(pkl_cd):
        with open(pkl_cd, 'rb') as f:
            sd: SectorDelta = pickle.load(f)
        return sd

    dict_sector_dist = dict()
    dict_sector_price = dict()
    # dictionary for id_code with key of code
    dict_id_code = get_dict_id_code()

    con = DBInfo.get_connection()
    if con.open():
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Initialize dictionary for 33業種区分
        set_13sector = set()
        sql = sql_sel_13sector_from_ticker()
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
            print(code)
            # _________________________________________________________________
            # 33業種区分
            name_13sector = ''
            sql = sql_sel_13sector_from_ticker_with_code(code)
            query = QSqlQuery(sql)
            if query.next():
                name_13sector = query.value(0)
            # _________________________________________________________________
            # day 1
            sql = sql_sel_close_from_trade_with_id_code_date(
                dict_id_code[code], pair_date[0]
            )
            query = QSqlQuery(sql)
            if query.next():
                close_1 = query.value(0)
            else:
                continue
            # _________________________________________________________________
            # day 2
            sql = sql_sel_close_from_trade_with_id_code_date(
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
        with open(pkl_cd, 'wb') as f:
            pickle.dump(sd, f)

        return sd
    else:
        print('Cannot open database')
        return None


def diff_close_open_by_sector(latest_date: int) -> Union[SectorDelta, None]:
    pkl_co = 'pool/close_open_%d.pkl' % latest_date
    if os.path.isfile(pkl_co):
        with open(pkl_co, 'rb') as f:
            sd: SectorDelta = pickle.load(f)
        return sd

    dict_sector_dist = dict()
    dict_sector_price = dict()
    # dictionary for id_code with key of code
    dict_id_code = get_dict_id_code()

    con = DBInfo.get_connection()
    if con.open():
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Initialize dictionary for 33業種区分
        set_13sector = set()
        sql = sql_sel_13sector_from_ticker()
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
            print(code)
            # _________________________________________________________________
            # 33業種区分
            name_13sector = ''
            sql = sql_sel_13sector_from_ticker_with_code(code)
            query = QSqlQuery(sql)
            if query.next():
                name_13sector = query.value(0)
            # _________________________________________________________________
            # latest day
            sql = sql_sel_open_close_from_trade_with_id_code_date(
                dict_id_code[code], latest_date
            )
            query = QSqlQuery(sql)
            if query.next():
                p_open = query.value(0)
                p_close = query.value(1)
            else:
                continue

            diff = p_close - p_open
            dict_sector_dist[name_13sector].append(diff)
            pair_price = [p_open, p_close]
            dict_sector_price[name_13sector].append(pair_price)
        con.close()

        sd = SectorDelta(dict_sector_dist, dict_sector_price)
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        with open(pkl_co, 'wb') as f:
            pickle.dump(sd, f)

        return sd
    else:
        print('Cannot open database')
        return None
