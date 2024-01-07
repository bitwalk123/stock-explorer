from funcs.tbl_currency import create_tbl_currency
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()

    # create ticker table
    result = create_tbl_currency()
    print(result)
