from funcs.tbl_currency import drop_tbl_currency
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    result = drop_tbl_currency()
    print(result)
