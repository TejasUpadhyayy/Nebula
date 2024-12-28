from web3 import Web3
import json
import hashlib
from datetime import datetime

class BlockchainManager:
    def __init__(self):
        # Connect to Sepolia testnet using Infura
        self.w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_INFURA_KEY'))
        
    def create_prediction_hash(self, symbol, current_price, predicted_price, timestamp):
        """Create a hash of the prediction data"""
        prediction_data = f"{symbol}-{current_price}-{predicted_price}-{timestamp}"
        return hashlib.sha256(prediction_data.encode()).hexdigest()
    
    def store_prediction(self, prediction_hash):
        """Store prediction hash on blockchain (simulated for now)"""
        # For now, we'll just print the hash
        print(f"\nPrediction stored on blockchain!")
        print(f"Hash: {prediction_hash}")
        return prediction_hash