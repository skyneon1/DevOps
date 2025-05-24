import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, List, Optional
import json
import os

class ThreatDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize ML model
        if model_path and os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
        
        self.scaler = StandardScaler()
        self.feature_columns = [
            'request_rate',
            'error_rate',
            'response_time',
            'payload_size',
            'unique_ips',
            'auth_failures'
        ]

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def preprocess_data(self, data: pd.DataFrame) -> np.ndarray:
        """Preprocess the input data for model prediction."""
        # Handle missing values
        data = data.fillna(data.mean())
        
        # Scale features
        scaled_data = self.scaler.fit_transform(data[self.feature_columns])
        return scaled_data

    def detect_threats(self, metrics: Dict) -> Dict:
        """Detect potential security threats using ML model."""
        try:
            # Convert metrics to DataFrame
            df = pd.DataFrame([metrics])
            
            # Preprocess data
            processed_data = self.preprocess_data(df)
            
            # Predict anomalies
            predictions = self.model.predict(processed_data)
            scores = self.model.score_samples(processed_data)
            
            # Calculate threat score (0-100)
            threat_score = self._calculate_threat_score(scores[0])
            
            # Determine threat level
            threat_level = self._determine_threat_level(threat_score)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "threat_score": threat_score,
                "threat_level": threat_level,
                "is_anomaly": bool(predictions[0] == -1),
                "confidence": float(abs(scores[0])),
                "metrics": metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error in threat detection: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }

    def _calculate_threat_score(self, anomaly_score: float) -> float:
        """Convert anomaly score to threat score (0-100)."""
        # Normalize score to 0-100 range
        normalized_score = (anomaly_score - self.model.offset_) / self.model.threshold_
        threat_score = max(0, min(100, normalized_score * 100))
        return threat_score

    def _determine_threat_level(self, threat_score: float) -> str:
        """Determine threat level based on score."""
        if threat_score >= 80:
            return "CRITICAL"
        elif threat_score >= 60:
            return "HIGH"
        elif threat_score >= 40:
            return "MEDIUM"
        elif threat_score >= 20:
            return "LOW"
        else:
            return "NORMAL"

    def train_model(self, historical_data: List[Dict]):
        """Train the model with historical data."""
        try:
            # Convert to DataFrame
            df = pd.DataFrame(historical_data)
            
            # Preprocess data
            processed_data = self.preprocess_data(df)
            
            # Train model
            self.model.fit(processed_data)
            
            # Save model
            joblib.dump(self.model, 'threat_detection_model.joblib')
            
            return {
                "status": "success",
                "message": "Model trained successfully",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    detector = ThreatDetector()
    
    # Example metrics
    metrics = {
        "request_rate": 100,
        "error_rate": 0.05,
        "response_time": 200,
        "payload_size": 1024,
        "unique_ips": 50,
        "auth_failures": 3
    }
    
    # Detect threats
    result = detector.detect_threats(metrics)
    print(json.dumps(result, indent=2)) 