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


import pandas as pd
import pathlib

def ts():
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S')

def safe_stamp():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def safe_filename(prefix: str, meta: dict) -> str:
    mid = "_".join([f"{k}-{str(v).replace(' ', '-')[:20]}" for k, v in meta.items()])
    return f"{prefix}_{mid}_{safe_stamp()}.csv"

def detect_format(path):
    path = str(path).lower()
    if path.endswith('.csv'):
        return 'csv'
    elif path.endswith(('.parquet', '.pq', '.parq')):
        return 'parquet'
    else:
        raise ValueError(f"Unsupported format for: {path}")

def write_df(df: pd.DataFrame, path):
    path = pathlib.Path(path)
    fmt = detect_format(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == 'csv':
        df.to_csv(path, index=False)
    else:
        df.to_parquet(path)
    return path

def read_df(path):
    path = pathlib.Path(path)
    fmt = detect_format(path)
    if fmt == 'csv':
        df = pd.read_csv(path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        return pd.read_parquet(path)
