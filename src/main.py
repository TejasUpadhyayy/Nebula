from src.data.stock_data import fetch_stock_data
from src.utils.indicators import add_technical_indicators
from src.utils.advanced_indicators import add_advanced_indicators
from src.models.predictor import train_prediction_model, make_predictions_multiple_timeframes
from src.utils.visualizer import plot_predictions
from src.utils.verification import PredictionVerifier
from src.utils.report_generator import ReportGenerator
from src.utils.portfolio_analyzer import PortfolioAnalyzer
import time

verifier = PredictionVerifier()
report_gen = ReportGenerator()
portfolio = PortfolioAnalyzer()

def show_stock_categories():
   categories = {
       "1": ("Tech", ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "META", "TSLA", "NFLX", "AMD", "INTC"]),
       "2": ("Finance", ["JPM", "BAC", "WFC", "C", "GS", "MS", "V", "MA"]),
       "3": ("Healthcare", ["JNJ", "PFE", "ABBV", "MRK", "UNH", "CVS"]),
       "4": ("Retail", ["WMT", "TGT", "COST", "HD", "LOW", "AMZN"]),
       "5": ("Energy", ["XOM", "CVX", "COP", "BP", "SHEL"])
   }
   
   while True:
       print("\nStock Categories:")
       for key, (category, stocks) in categories.items():
           print(f"{key}. {category}")
       print("6. Enter custom symbol")
       print("7. Back to main menu")
       
       choice = input("\nSelect category (1-7): ")
       
       if choice in categories:
           cat_name, stocks = categories[choice]
           print(f"\n{cat_name} Stocks:")
           for i, stock in enumerate(stocks, 1):
               print(f"{i}. {stock}")
           
           stock_choice = input("\nSelect stock number (or 'b' for back): ")
           if stock_choice.lower() == 'b':
               continue
           try:
               return stocks[int(stock_choice)-1]
           except:
               print("Invalid selection")
               
       elif choice == '6':
           symbol = input("Enter stock symbol: ").upper()
           return symbol
       elif choice == '7':
           return None
       else:
           print("Invalid choice")

def analyze_stock_advanced(symbol):
    try:
        print(f"\nPerforming advanced analysis for {symbol}...")
        df = fetch_stock_data(symbol)
        
        if df is not None:
            df = add_technical_indicators(df)
            df = add_advanced_indicators(df)
            
            model = train_prediction_model(df)
            latest_data = df[['Close', 'SMA_20', 'RSI']].iloc[-1]
            timeframe_predictions = make_predictions_multiple_timeframes(model, latest_data)
            
            current_price = df['Close'].iloc[-1]
            prediction_hash = verifier.store_prediction(symbol, current_price, timeframe_predictions['next_day'])
            
            return {
                "current_price": current_price,
                "predictions": timeframe_predictions,
                "indicators": {
                    "RSI": df['RSI'].iloc[-1],
                    "MACD": df['MACD'].iloc[-1]
                },
                "prediction_hash": prediction_hash,
                "dates": df.index.tolist()[-30:],
                "prices": df['Close'].tolist()[-30:]
            }
            
    except Exception as e:
        print(f"Error analyzing {symbol}: {str(e)}")
        return None

def manage_portfolio():
   while True:
       print("\n=== Portfolio Management ===")
       print("1. Add stock to portfolio")
       print("2. View portfolio")
       print("3. Analyze portfolio")
       print("4. Return to main menu")
       
       choice = input("\nEnter your choice (1-4): ")
       
       if choice == '1':
           symbol = input("Enter stock symbol: ").upper()
           try:
               shares = float(input("Enter number of shares: "))
               price = float(input("Enter purchase price per share: "))
               portfolio.add_stock(symbol, shares, price)
               print(f"\nAdded {shares} shares of {symbol} at ${price:.2f}")
           except ValueError:
               print("Invalid input. Please enter numeric values.")
               
       elif choice == '2':
           if not portfolio.portfolio:
               print("Portfolio is empty!")
           else:
               print("\n=== Current Portfolio ===")
               for symbol, data in portfolio.portfolio.items():
                   print(f"{symbol}: {data['shares']} shares at ${data['purchase_price']:.2f}")
                   
       elif choice == '3':
           if not portfolio.portfolio:
               print("Portfolio is empty!")
           else:
               print("\nAnalyzing portfolio...")
               for symbol in portfolio.portfolio:
                   analyze_stock_advanced(symbol)
                   
       elif choice == '4':
           break

def main():
   while True:
       print("\n=== Neural-Blockchain Stock Prediction System ===")
       print("1. Analyze a specific stock")
       print("2. Analyze popular tech stocks")
       print("3. Manage portfolio")
       print("4. Verify previous prediction")
       print("5. Exit")
       
       try:
           choice = input("\nEnter your choice (1-5): ")
           
           if choice == '1':
               symbol = show_stock_categories()
               if symbol:
                   analyze_stock_advanced(symbol)
           
           elif choice == '2':
               symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'AMD', 'INTC']
               for symbol in symbols:
                   analyze_stock_advanced(symbol)
                   time.sleep(1)  # Prevent too many rapid requests
           
           elif choice == '3':
               manage_portfolio()
           
           elif choice == '4':
               hash_id = input("Enter the prediction hash to verify: ")
               prediction_data = verifier.verify_prediction(hash_id)
               if prediction_data:
                   print("\n=== Verified Prediction Data ===")
                   for key, value in prediction_data.items():
                       print(f"{key}: {value}")
               else:
                   print("Prediction not found!")
           
           elif choice == '5':
               print("\nThank you for using the Neural-Blockchain Stock Prediction System!")
               break
           
           else:
               print("Invalid choice. Please try again.")
           
       except Exception as e:
           print(f"An error occurred: {str(e)}")
           print("Please try again.")
       
       input("\nPress Enter to continue...")

if __name__ == "__main__":
   main()