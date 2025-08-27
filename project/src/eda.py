# /src/eda.py
import numpy as np
from scipy.stats import skew, kurtosis

def eda_summary(df, numeric_cols=None):
    """Quick numeric profiling and missingness summary."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    out = {}
    out['shape'] = df.shape
    out['dtypes'] = df.dtypes.to_dict()
    out['missing'] = df.isna().sum().to_dict()
    
    profile = df[numeric_cols].describe().T
    profile['skew'] = [skew(df[c].dropna()) for c in numeric_cols]
    profile['kurtosis'] = [kurtosis(df[c].dropna()) for c in numeric_cols]
    out['numeric_profile'] = profile
    return out
