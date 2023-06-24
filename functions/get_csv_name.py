import os


def get_csv_name(code: int) -> str:
    return '%s.csv' % os.path.join('data', '%d.T' % code)
