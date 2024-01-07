from funcs.tbl_exchange import (
    create_tbl_exchange,
    init_tbl_exchange,
)
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()

    # create exchange table
    result = create_tbl_exchange()
    print(result)

    # initialize exchange table
    result = init_tbl_exchange()
    print(result)
