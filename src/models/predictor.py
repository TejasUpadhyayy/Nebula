from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

def prepare_data_for_training(df):
    """Prepare data for model training"""
    # Create a copy of the dataframe
    df = df.copy()
    
    # Create target (next day's price)
    df['Target'] = df['Close'].shift(-1)
    
    # Select features
    features = ['Close', 'SMA_20', 'RSI']
    
    # Drop any rows with NaN values
    df = df.dropna()
    
    # Prepare X (features) and y (target)
    X = df[features]
    y = df['Target']
    
    # Remove the last row since it won't have a target value
    X = X[:-1]
    y = y[:-1]
    
    return X, y

def train_prediction_model(df):
    """Train a RandomForest model"""
    # Prepare data
    X, y = prepare_data_for_training(df)
    
    # Create and train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model

def make_prediction(model, latest_data):
    """Make prediction using trained model"""
    return model.predict([latest_data])[0]

def make_predictions_multiple_timeframes(model, latest_data):
    """Make predictions for multiple timeframes"""
    predictions = {
        'next_day': model.predict([latest_data])[0],
        'next_week': None,
        'next_month': None
    }
    
    # Simulate longer timeframe predictions
    # (In reality, you'd want different models for different timeframes)
    predictions['next_week'] = predictions['next_day'] * (1 + (np.random.random() - 0.5) * 0.1)
    predictions['next_month'] = predictions['next_week'] * (1 + (np.random.random() - 0.5) * 0.2)
    
    return predictions