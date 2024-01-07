from funcs.tbl_trade import (
    create_tbl_trade,
    init_tbl_trade,
)
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()

    # create trade table
    result = create_tbl_trade()
    print(result)

    # initialize trade table
    result = init_tbl_trade()
    print(result)
