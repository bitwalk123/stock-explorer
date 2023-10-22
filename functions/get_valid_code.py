from functions.app_enum import PreProcessExcluded
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dict_code import get_dict_code
from functions.preprocess import PreProcess


def get_valid_code(start: int, end: int) -> tuple:
    # valid list of id_code
    list_valid_id_code = list()
    list_target_id_code = list()
    num_total = 0
    # prepare dictionary for id_code and code
    dict_code: dict = get_dict_code()
    for id_code in dict_code.keys():
        code = dict_code[id_code]
        prep = PreProcess(id_code, start, end)

        if prep.IsExclude():
            num_total += 1
            print('%d.T is excluded : ' % code, end='')

            if prep.FLAG_EXCLUDE == PreProcessExcluded.EMPTY:
                print('No Data!')
            elif prep.FLAG_EXCLUDE == PreProcessExcluded.FEW:
                print(
                    'Few data =',
                    prep.data_n,
                    '<',
                    prep.minimum_n,
                    '(Minimum size)'
                )
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
            list_valid_id_code.append(id_code)
            if prep.IsTarget():
                print(
                    '%d.T is target: Open(Median) = %.1f JPY, Volume(Median) = %d' % (
                        code,
                        prep.open_median,
                        prep.volume_median,
                    )
                )
                list_target_id_code.append(id_code)

    print('excluded %d out of %d tickers' % (num_total, len(dict_code.keys())))
    return dict_code, list_valid_id_code, list_target_id_code
