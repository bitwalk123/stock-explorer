from funcs.common import write_json, read_json

if __name__ == '__main__':
    file_json = 'ini_trial.json'
    # file_json = 'ini_test.json'
    # file_json = 'stock-explorer.json'

    dict_init = dict()
    dict_init['driver'] = 'QPSQL'
    dict_init['host'] = '192.168.0.34'
    dict_init['db_name'] = 'testdb'
    # dict_init['db_name'] = 'stock-explorer'
    dict_init['user'] = 'postgres'
    dict_init['password'] = 'postgres'
    dict_init['tse'] = 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls'

    write_json(dict_init, file_json)

    dict_init = read_json(file_json)
    print(dict_init)
