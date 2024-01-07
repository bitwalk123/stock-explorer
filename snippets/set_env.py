from funcs.common import read_json
from structs.db_info import DBInfo


def set_env() -> dict:
    file_json = 'ini_my.json'
    return set_info_dict(file_json)


def set_info_dict(file_json):
    dict_info = read_json(file_json)
    DBInfo.setInfoDict(dict_info)
    return dict_info
