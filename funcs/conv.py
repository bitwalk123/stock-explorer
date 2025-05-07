import re


def conv_jpx(symbol) -> str:
    """
    東証の銘柄コードであれば末尾に .T を付加する

    :param symbol:
    :return:
    """
    pattern = re.compile(r'^[1-9]{1}[0-9]{2}[0-9A-Z]{1}$')
    m = pattern.match(symbol)
    if m:
        symbol = '%s.T' % symbol

    return symbol
