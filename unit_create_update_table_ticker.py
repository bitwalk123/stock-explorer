from funcs.tbl_ticker import (
    create_tbl_ticker,
    update_tbl_ticker,
)
from snippets.set_env import set_env
from structs.res import AppRes

if __name__ == '__main__':
    dict_info = set_env()
    res = AppRes()

    # create ticker table
    result = create_tbl_ticker()
    print(result)

    # update ticker info
    tse = res.getTSE()
    result = update_tbl_ticker(tse)
    print(result)
