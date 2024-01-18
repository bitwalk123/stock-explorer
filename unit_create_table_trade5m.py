from funcs.tbl_trade5m import create_tbl_trade5m
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()

    # create trade table
    result = create_tbl_trade5m()
    print(result)
