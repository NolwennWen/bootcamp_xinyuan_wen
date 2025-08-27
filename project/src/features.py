# /src/features.py
import pandas as pd
import numpy as np

def create_stock_features(df):
    """Feature engineering for stock prediction."""
    df['daily_return'] = df['close'].pct_change().fillna(0)
    df['log_return'] = np.log(df['close'] / df['close'].shift(1)).fillna(0)
    df['volatility_5d'] = df['daily_return'].rolling(5).std().fillna(0)
    df['ma_5'] = df['close'].rolling(5).mean().fillna(df['close'])
    df['ma_20'] = df['close'].rolling(20).mean().fillna(df['close'])
    df['ma_spread'] = df['ma_5'] - df['ma_20']
    df['vol_mean_5'] = df['volume'].rolling(5).mean().fillna(df['volume'])
    df['hl_spread'] = df['high'] - df['low']
    df['co_diff'] = df['close'] - df['open']

    # RSI 14-day
    window = 14
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    roll_up = pd.Series(gain).rolling(window).mean()
    roll_down = pd.Series(loss).rolling(window).mean()
    rs = roll_up / roll_down
    df['rsi'] = 100 - (100 / (1 + rs))
    df['rsi'] = df['rsi'].fillna(50)

    # Momentum
    df['momentum_5'] = df['close'] - df['close'].shift(5)
    df['momentum_5'] = df['momentum_5'].fillna(0)
    
    # Log volume
    df['log_volume'] = np.log(df['vol_mean_5'] + 1)
    
    # RSI MA5
    df['rsi_ma5'] = df['rsi'].rolling(5).mean()
    
    return df
