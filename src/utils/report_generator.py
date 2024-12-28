from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        # Create reports directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')
    
    def generate_report(self, symbol, current_price, predicted_price, rsi, sma, prediction_hash):
        """Generate a professional-looking analysis report"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"reports/{symbol}_analysis_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("=================================================\n")
            f.write("        STOCK MARKET PREDICTION ANALYSIS          \n")
            f.write("=================================================\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Stock Symbol: {symbol}\n\n")
            f.write("PRICE ANALYSIS\n")
            f.write("-------------------------------------------------\n")
            f.write(f"Current Price: ${current_price:.2f}\n")
            f.write(f"Predicted Next Price: ${predicted_price:.2f}\n")
            f.write(f"Predicted Change: {((predicted_price-current_price)/current_price)*100:.2f}%\n\n")
            f.write("TECHNICAL INDICATORS\n")
            f.write("-------------------------------------------------\n")
            f.write(f"RSI (14-day): {rsi:.2f}\n")
            f.write(f"20-day Moving Average: ${sma:.2f}\n\n")
            f.write("VERIFICATION\n")
            f.write("-------------------------------------------------\n")
            f.write(f"Prediction Hash: {prediction_hash}\n\n")
            f.write("INTERPRETATION\n")
            f.write("-------------------------------------------------\n")
            
            # Add basic interpretation
            rsi_analysis = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
            trend = "Above" if current_price > sma else "Below"
            
            f.write(f"RSI Status: {rsi_analysis}\n")
            f.write(f"Price is {trend} 20-day Moving Average\n\n")
            f.write("=================================================\n")
            f.write("DISCLAIMER: This is for educational purposes only.\n")
            f.write("Do not use this for actual trading decisions.\n")
            f.write("=================================================\n")
        
        return filename