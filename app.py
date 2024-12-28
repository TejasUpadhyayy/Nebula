from flask import Flask, render_template, request, jsonify, Response
from fpdf import FPDF
from datetime import datetime
import sys, os
from src.sentiment.analyzer import SentimentAnalyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import analyze_stock_advanced

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
   try:
       symbol = request.form['symbol']
       result = analyze_stock_advanced(symbol)
       
       if result:
           return jsonify({
               "success": True,
               "current_price": result['current_price'],
               "predictions": {
                   "next_day": result['predictions']['next_day'],
                   "next_week": result['predictions']['next_week'],
                   "next_month": result['predictions']['next_month']
               },
               "indicators": {
                   "rsi": float(result['indicators']['RSI']),
                   "macd": float(result['indicators']['MACD'])
               },
               "hash": result['prediction_hash'],
               "chart_data": {
                   "dates": result['dates'],
                   "prices": result['prices'].tolist() if hasattr(result['prices'], 'tolist') else result['prices']
               }
           })
       return jsonify({"success": False, "message": f"Failed to analyze {symbol}"})
   except Exception as e:
       print(f"Error in analyze route: {str(e)}")
       return jsonify({"success": False, "message": str(e)})

@app.route('/export-pdf/<symbol>')
def export_pdf(symbol):
   try:
       result = analyze_stock_advanced(symbol)
       pdf = FPDF()
       pdf.add_page()

       # Header with logo/styling
       pdf.set_font('Arial', 'B', 24)
       pdf.set_text_color(44, 62, 80)
       pdf.cell(0, 20, 'Stock Analysis Report', ln=True, align='C')
       
       # Stock Info Section
       pdf.set_font('Arial', 'B', 18)
       pdf.set_text_color(52, 73, 94)
       pdf.cell(0, 15, f'{symbol} Stock Analysis', ln=True)
       
       # Current Price & Predictions
       pdf.set_font('Arial', '', 12)
       pdf.set_text_color(0, 0, 0)
       pdf.cell(0, 10, f"Current Price: ${result['current_price']:.2f}", ln=True)
       
       pdf.set_font('Arial', 'B', 14)
       pdf.cell(0, 15, 'Price Predictions', ln=True)
       pdf.set_font('Arial', '', 12)
       pdf.cell(0, 8, f"Next Day: ${result['predictions']['next_day']:.2f}", ln=True)
       pdf.cell(0, 8, f"Next Week: ${result['predictions']['next_week']:.2f}", ln=True)
       pdf.cell(0, 8, f"Next Month: ${result['predictions']['next_month']:.2f}", ln=True)

       # Technical Analysis
       pdf.ln(10)
       pdf.set_font('Arial', 'B', 14)
       pdf.cell(0, 15, 'Technical Indicators', ln=True)
       pdf.set_font('Arial', '', 12)
       pdf.cell(0, 8, f"RSI (14): {result['indicators']['RSI']:.2f}", ln=True)
       pdf.cell(0, 8, f"MACD: {result['indicators']['MACD']:.2f}", ln=True)

       # Add chart
       pdf.ln(10)
       pdf.set_font('Arial', 'B', 14)
       pdf.cell(0, 15, 'Price Chart', ln=True)
       
       # Generate chart image using matplotlib
       import matplotlib.pyplot as plt
       plt.figure(figsize=(10, 6))
       plt.plot(result['dates'][-30:], result['prices'][-30:], color='#3498db')
       plt.title(f'{symbol} Price History (Last 30 Days)')
       plt.grid(True)
       plt.xticks(rotation=45)
       chart_path = f'temp_{symbol}_chart.png'
       plt.savefig(chart_path, bbox_inches='tight')
       plt.close()
       
       # Add chart to PDF
       pdf.image(chart_path, x=10, w=190)
       os.remove(chart_path)  # Clean up temp file

       # Verification section
       pdf.ln(10)
       pdf.set_font('Arial', 'B', 14)
       pdf.cell(0, 15, 'Blockchain Verification', ln=True)
       pdf.set_font('Arial', '', 10)
       pdf.cell(0, 8, f"Hash: {result['prediction_hash']}", ln=True)

       # Footer
       pdf.set_y(-30)
       pdf.set_font('Arial', 'I', 8)
       pdf.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')

       buffer = bytes(pdf.output())
       return Response(
           buffer,
           mimetype='application/pdf',
           headers={'Content-Disposition': f'attachment;filename={symbol}_analysis.pdf'}
       )
   except Exception as e:
       print(f"PDF Export Error: {str(e)}")
       return str(e), 400
   
@app.route('/sentiment/<symbol>')
def get_sentiment(symbol):
    analyzer = SentimentAnalyzer()
    result = analyzer.get_sentiment(symbol)
    return jsonify(result) 

if __name__ == '__main__':
   app.run(debug=True)