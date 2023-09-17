from functions.get_dict_code import get_dict_code
from functions.get_info_ticker import get_info_ticker
from functions.resources import get_connection


def main():
    dict_code = dict()
    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        dict_code = get_dict_code()
        con.close()

    for id_code in dict_code.keys():
        code = dict_code[id_code]
        get_info_ticker(code)
        print(code)


if __name__ == "__main__":
    main()
