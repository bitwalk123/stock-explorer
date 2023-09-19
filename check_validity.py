import datetime as dt

from functions.app_enum import PreProcsExcl
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dict_code import get_dict_code
from functions.preprocess import PreProcess
from functions.resources import get_connection


def main():
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone

    start_str = '2022-01-04'
    start_dt = dt.datetime.strptime(start_str, '%Y-%m-%d')
    start = int(dt.datetime.timestamp(start_dt)) + tz_delta
    end_dt = dt.datetime.now()
    end = int(dt.datetime.timestamp(end_dt)) + tz_delta
    print(start, conv_timestamp2date(start), '-', end, conv_timestamp2date(end))

    # valid list of id_code
    list_id_code = list()
    dict_code = dict()
    num_total = 0

    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        dict_code: dict = get_dict_code()

        for id_code in dict_code.keys():
            code = dict_code[id_code]
            preprcs = PreProcess(id_code, start, end)
            if preprcs.exclude():
                num_total += 1

                print('%d.T : ' % code, end='')
                if preprcs.flag_exclude == PreProcsExcl.EMPTY:
                    print('No Data!')
                elif preprcs.flag_exclude == PreProcsExcl.VOLUME:
                    print(
                        'Volume(Median) =',
                        preprcs.volume_median,
                    )
                elif preprcs.flag_exclude == PreProcsExcl.SPLIT:
                    print(
                        'Volume(Median) =',
                        preprcs.volume_median,
                        'Split',
                        conv_timestamp2date(preprcs.date),
                        preprcs.price_open_pre, '>>',
                        preprcs.price_open, ':',
                        preprcs.price_open - preprcs.price_open_pre,
                    )
                else:
                    print('Unknown')
            else:
                list_id_code.append(id_code)
        con.close()
    else:
        print('fail to open db.')

    print('excluded %d / %d' % (num_total, len(dict_code.keys())))
    print('valid number of id_code : %d' % len(list_id_code))


if __name__ == "__main__":
    main()
