def add_advanced_indicators(df):
    """Add advanced technical indicators"""
    df = df.copy()
    
    # MACD (Moving Average Convergence Divergence)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands (20-day, 2 standard deviations)
    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
    df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
    
    # Stochastic Oscillator
    lookback = 14
    df['14H'] = df['High'].rolling(lookback).max()
    df['14L'] = df['Low'].rolling(lookback).min()
    df['%K'] = (df['Close'] - df['14L']) * 100/(df['14H'] - df['14L'])
    df['%D'] = df['%K'].rolling(3).mean()
    
    return df