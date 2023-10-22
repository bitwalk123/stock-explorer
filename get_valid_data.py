import datetime as dt

from functions.app_enum import PreProcessEnum
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dict_code import get_dict_code
from functions.preprocess import PreProcess
from functions.resources import get_connection


def main():
    day1 = 24 * 60 * 60
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    now_dt = dt.datetime.now()
    now = int(dt.datetime.timestamp(now_dt)) + tz_delta
    end = (now // day1 - 1) * day1
    start = end - 365 * day1
    print(
        'date scope :',
        dt.datetime.fromtimestamp(start),
        '-',
        dt.datetime.fromtimestamp(end)
    )

    # valid list of id_code
    list_id_code = list()
    num_total = 0

    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        dict_code: dict = get_dict_code()
        for id_code in list(dict_code.keys()):
            code = dict_code[id_code]
            preprocess = PreProcess(id_code, start, end)

            if preprocess.exclude():
                num_total += 1
                print('%d.T : ' % code, end='')

                if preprocess.flag_exclude == PreProcessEnum.EMPTY:
                    print('No Data!')
                elif preprocess.flag_exclude == PreProcessEnum.VOLUME:
                    print(
                        'Volume(Median) =',
                        preprocess.volume_median,
                    )
                elif preprocess.flag_exclude == PreProcessEnum.SPLIT:
                    print(
                        'Volume(Median) =',
                        preprocess.volume_median,
                        'Split',
                        conv_timestamp2date(preprocess.date),
                        preprocess.price_open_pre, '>>',
                        preprocess.price_open, ':',
                        preprocess.price_open - preprocess.price_open_pre,
                    )
                else:
                    print('Unknown')
            else:
                list_id_code.append(id_code)

        con.close()
    else:
        print('fail to open db.')


if __name__ == "__main__":
    main()
