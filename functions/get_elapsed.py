import time


def get_elapsed(time_start: float) -> float:
    """Get elapsed time in second.

    Args:
        time_start (float): start time

    Returns:
        float: elapsed time in seconds
    """
    time_end = time.time()
    # elapsed seconds
    elapsed = (time_end - time_start)
    return elapsed
