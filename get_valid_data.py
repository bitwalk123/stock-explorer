import datetime as dt

from functions.app_enum import PreProcessExcluded
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
    dict_code = dict()
    num_total = 0

    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        dict_code: dict = get_dict_code()
        for id_code in dict_code.keys():
            code = dict_code[id_code]
            prep = PreProcess(id_code, start, end)

            if prep.exclude():
                num_total += 1
                print('%d.T is excluded : ' % code, end='')

                if prep.FLAG_EXCLUDE == PreProcessExcluded.EMPTY:
                    print('No Data!')
                elif prep.FLAG_EXCLUDE == PreProcessExcluded.VOLUME:
                    print(
                        'Volume(Median) =',
                        prep.volume_median,
                    )
                elif prep.FLAG_EXCLUDE == PreProcessExcluded.SPLIT:
                    print(
                        'Volume(Median) =',
                        prep.volume_median,
                        'Split',
                        conv_timestamp2date(prep.date),
                        prep.price_open_pre, '>>',
                        prep.price_open, ':',
                        prep.price_open - prep.price_open_pre,
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
