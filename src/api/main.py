from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from datetime import datetime

# Import our existing analysis code
from ..data.stock_data import fetch_stock_data
from ..utils.indicators import add_technical_indicators
from ..utils.advanced_indicators import add_advanced_indicators
from ..models.predictor import train_prediction_model, make_predictions_multiple_timeframes
from ..utils.verification import PredictionVerifier

app = FastAPI(title="Stock Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    symbol: str

@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    try:
        df = fetch_stock_data(request.symbol)
        if df is None:
            raise HTTPException(status_code=404, detail="Stock data not found")
            
        # Add indicators
        df = add_technical_indicators(df)
        df = add_advanced_indicators(df)
        
        # Get predictions
        model = train_prediction_model(df)
        latest_data = df[['Close', 'SMA_20', 'RSI']].iloc[-1]
        predictions = make_predictions_multiple_timeframes(model, latest_data)
        
        # Get current price and indicators
        current_data = {
            'price': df['Close'].iloc[-1],
            'rsi': df['RSI'].iloc[-1],
            'macd': df['MACD'].iloc[-1],
            'signal_line': df['Signal_Line'].iloc[-1],
            'stoch_k': df['%K'].iloc[-1],
            'stoch_d': df['%D'].iloc[-1]
        }
        
        return {
            "symbol": request.symbol,
            "current_data": current_data,
            "predictions": predictions,
            "timestamp": datetime.now().isoformat()
        }
    
        # Add blockchain verification
        verifier = PredictionVerifier()
        prediction_hash = verifier.store_prediction(
            request.symbol,
            current_data['price'],
            predictions['next_day']
        )
        
        return {
            "symbol": request.symbol,
            "current_data": current_data,
            "predictions": predictions,
            "blockchain_verification": {
                "hash": prediction_hash,
                "timestamp": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)