import os


def delete_file(filename: str) -> bool:
    """Delete specified filename
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True
    else:
        return False
