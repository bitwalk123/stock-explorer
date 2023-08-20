import os


def get_ini_file() -> str:
    """Get name of ini file
    """
    # Name of ini file depends on OS.
    """
    if platform.system() == 'Windows':
        file_config = 'stock_explorer.ini'
    else:
        file_config = '.stock_explorer'
    """
    file_config = '.stock_explorer'

    # ini file in full path
    # return os.path.join(expanduser('~'), file_config)
    return os.path.join(os.getcwd(), file_config)
