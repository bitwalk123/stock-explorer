import os


def delete_file(filename: str) -> bool:
    if os.path.exists(filename):
        os.remove(filename)
        return True
    else:
        return False
