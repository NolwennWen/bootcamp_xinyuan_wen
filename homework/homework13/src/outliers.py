# src/outliers.py

import pandas as pd
import numpy as np

def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Detect outliers using the Interquartile Range (IQR) method.

    Parameters
    ----------
    series : pd.Series
        Numeric series to evaluate.
    k : float
        Multiplier for IQR to define outlier fences (default 1.5).

    Returns
    -------
    pd.Series
        Boolean mask: True indicates an outlier.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - k * iqr
    upper_fence = q3 + k * iqr
    return (series < lower_fence) | (series > upper_fence)


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using Z-score method.

    Parameters
    ----------
    series : pd.Series
        Numeric series to evaluate.
    threshold : float
        Z-score threshold to classify outliers (default 3.0).

    Returns
    -------
    pd.Series
        Boolean mask: True indicates an outlier.
    """
    mean = series.mean()
    std = series.std(ddof=0)
    z_scores = (series - mean) / (std if std != 0 else 1.0)
    return z_scores.abs() > threshold


def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """
    Return a winsorized copy of the series, clipping to specified quantiles.

    Parameters
    ----------
    series : pd.Series
        Numeric series to winsorize.
    lower : float
        Lower quantile (default 0.05)
    upper : float
        Upper quantile (default 0.95)

    Returns
    -------
    pd.Series
        Winsorized series.
    """
    lower_val = series.quantile(lower)
    upper_val = series.quantile(upper)
    return series.clip(lower=lower_val, upper=upper_val)


def detect_outliers_dataframe(df: pd.DataFrame, numeric_cols: list, method: str = "iqr", **kwargs) -> pd.DataFrame:
    """
    Detect outliers for multiple numeric columns in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    numeric_cols : list
        List of numeric columns to check.
    method : str
        Method to use: 'iqr' or 'zscore'.
    kwargs : dict
        Additional parameters passed to the method.

    Returns
    -------
    pd.DataFrame
        DataFrame of boolean masks for each column, True indicates an outlier.
    """
    outlier_df = pd.DataFrame(index=df.index)
    for col in numeric_cols:
        if method.lower() == "iqr":
            outlier_df[f"{col}_outlier_iqr"] = detect_outliers_iqr(df[col], **kwargs)
        elif method.lower() == "zscore":
            outlier_df[f"{col}_outlier_z"] = detect_outliers_zscore(df[col], **kwargs)
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'.")
    return outlier_df
