# src/cleaning.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def fill_missing_median(df, columns=None):
    """Fill missing numeric values with median."""
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def drop_missing(df, columns=None, threshold=None):
    """Drop rows with missing values. Either subset columns or threshold fraction of non-NA required."""
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    if threshold is not None:
        return df_copy.dropna(thresh=int(threshold*df_copy.shape[1]))
    return df_copy.dropna()

def normalize_data(df, columns=None, method='minmax'):
    """Normalize numeric columns using MinMaxScaler or StandardScaler."""
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    if method=='minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy

def correct_column_types(df):
    """Fix column types: convert price string to float, date string to datetime, category to categorical lowercase."""
    df_copy = df.copy()
    if 'price' in df_copy.columns:
        df_copy['price'] = df_copy['price'].str.replace('$','').astype(float)
    if 'date_str' in df_copy.columns:
        df_copy['date'] = pd.to_datetime(df_copy['date_str'], errors='coerce')
    if 'category' in df_copy.columns:
        df_copy['category'] = df_copy['category'].str.lower().astype('category')
    return df_copy

def preprocess_df(df):
    """
    Comprehensive preprocessing: 
    fill missing values, drop rows, normalize numeric columns, correct column types.
    """
    df_clean = df.copy()
    df_clean = fill_missing_median(df_clean)
    df_clean = drop_missing(df_clean, threshold=0.5)
    df_clean = normalize_data(df_clean)
    df_clean = correct_column_types(df_clean)
    return df_clean
