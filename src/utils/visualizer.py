import matplotlib.pyplot as plt
import seaborn as sns

def plot_predictions(df, symbol, prediction):
    plt.figure(figsize=(12, 6))
    
    # Plot actual prices
    plt.plot(df.index[-30:], df['Close'][-30:], label='Actual Price', color='blue')
    
    # Add prediction point
    last_date = df.index[-1]
    plt.scatter(last_date, prediction, color='red', s=100, label='Prediction')
    
    plt.title(f'{symbol} Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f'{symbol}_prediction.png')
    print(f"Chart saved as {symbol}_prediction.png")