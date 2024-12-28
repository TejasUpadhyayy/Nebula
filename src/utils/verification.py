import hashlib
import json
from datetime import datetime

class PredictionVerifier:
    def __init__(self):
        self.prediction_store = {}  # Simulates blockchain storage
        
    def create_prediction_hash(self, data):
        """Create a unique hash for prediction"""
        timestamp = datetime.now().isoformat()
        data['timestamp'] = timestamp
        
        # Create a sorted string representation of data for consistent hashing
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def store_prediction(self, symbol, current_price, predicted_price):
        """Store prediction with verification"""
        prediction_data = {
            'symbol': symbol,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'prediction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Create hash
        prediction_hash = self.create_prediction_hash(prediction_data)
        
        # Store in our simulated blockchain
        self.prediction_store[prediction_hash] = prediction_data
        
        return prediction_hash
    
    def verify_prediction(self, hash_id):
        """Verify a prediction exists"""
        return self.prediction_store.get(hash_id)