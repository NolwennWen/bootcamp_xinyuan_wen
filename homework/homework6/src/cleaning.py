"""
cleaning.py

This module contains reusable data cleaning functions for Homework 6.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def fill_missing_median(df, columns=None):
    """
    Fill missing values in numeric columns with the median.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        columns (list, optional): List of numeric columns to fill. Defaults to all numeric.
        
    Returns:
        pd.DataFrame: DataFrame with missing values filled
    """
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def drop_missing(df, columns=None, threshold=None):
    """
    Drop rows with missing values based on columns or threshold.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        columns (list, optional): Subset of columns to check for missing values
        threshold (float, optional): Minimum fraction of non-missing values required
        
    Returns:
        pd.DataFrame: DataFrame with rows dropped
    """
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    if threshold is not None:
        return df_copy.dropna(thresh=int(threshold*df_copy.shape[1]))
    return df_copy.dropna()

def normalize_data(df, columns=None, method='minmax'):
    """
    Normalize numeric columns using MinMaxScaler or StandardScaler.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        columns (list, optional): Columns to normalize. Defaults to all numeric.
        method (str): 'minmax' or 'standard'
        
    Returns:
        pd.DataFrame: Normalized DataFrame
    """
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
    """
    Convert price to float, date_str to datetime, and category to lowercase category type.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with corrected types
    """
    df_copy = df.copy()
    if 'price' in df_copy.columns:
        df_copy['price'] = pd.to_numeric(df_copy['price'].astype(str).str.replace('$',''), errors='coerce')
    if 'date_str' in df_copy.columns:
        df_copy['date'] = pd.to_datetime(df_copy['date_str'], errors='coerce')
    if 'category' in df_copy.columns:
        df_copy['category'] = df_copy['category'].str.lower().astype('category')
    return df_copy
