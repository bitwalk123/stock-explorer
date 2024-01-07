from funcs.tbl_trade import drop_tbl_trade
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    result = drop_tbl_trade()
    print(result)
