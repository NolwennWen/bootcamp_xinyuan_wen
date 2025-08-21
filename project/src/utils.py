# src/utils.py

import numpy as np
from datetime import datetime

def calc_mean_std(lst):
    """
    Calculate mean and standard deviation of a list or array.

    Parameters
    ----------
    lst : list or np.array
        Numeric data to summarize.

    Returns
    -------
    tuple
        mean, standard deviation
    """
    arr = np.array(lst)
    return arr.mean(), arr.std()


def log_call(func):
    """
    Decorator to log the time when a function is called.

    Usage:
        @log_call
        def your_function(...):
            ...

    Parameters
    ----------
    func : callable
        Function to wrap.

    Returns
    -------
    callable
        Wrapped function with logging.
    """
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} called at {datetime.now()}")
        return func(*args, **kwargs)
    return wrapper


@log_call
def calc_mean_std_logged(lst):
    """
    Calculate mean and std of a list with logging of call time.

    Parameters
    ----------
    lst : list or np.array
        Numeric data to summarize.

    Returns
    -------
    tuple
        mean, standard deviation
    """
    return calc_mean_std(lst)
