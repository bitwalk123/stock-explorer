from funcs.tbl_exchange import drop_tbl_exchange
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    result = drop_tbl_exchange()
    print(result)
