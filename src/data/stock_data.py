import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL' for Apple)
        period: Time period (e.g., '1y' for 1 year)
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        df = ticker.history(period=period)
        
        # Basic data cleaning
        df = df.dropna()  # Remove any missing values
        
        print(f"Successfully fetched data for {symbol}")
        return df
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None