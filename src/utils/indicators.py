import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic technical indicators to the dataframe"""
    
    # Copy dataframe to avoid modifying original
    df = df.copy()
    
    # 1. Simple Moving Average (20 days)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # 2. Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df