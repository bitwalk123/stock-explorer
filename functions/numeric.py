def is_num(str_float: str) -> bool:
    try:
        float(str_float)
    except ValueError:
        return False
    else:
        return True
