from funcs.tbl_iticker import create_tbl_iticker
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()

    # create ticker table
    result = create_tbl_iticker()
    print(result)
