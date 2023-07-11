import os


def get_csv_name(code: int) -> str:
    """Get CSV file name for downloaded ticker filr
    """
    return '%s.csv' % os.path.join('data', '%d.T' % code)
