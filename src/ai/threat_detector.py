import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd
import logging
from datetime import datetime
import json

class ThreatDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def preprocess_logs(self, logs):
        """Convert log data into features for the model."""
        features = []
        for log in logs:
            feature_vector = [
                log.get('request_count', 0),
                log.get('error_count', 0),
                log.get('response_time', 0),
                log.get('payload_size', 0)
            ]
            features.append(feature_vector)
        return np.array(features)

    def train(self, historical_logs):
        """Train the anomaly detection model."""
        try:
            features = self.preprocess_logs(historical_logs)
            self.model.fit(features)
            self.logger.info("Model trained successfully")
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}")
            raise

    def detect_threats(self, current_logs):
        """Detect potential threats in current logs."""
        try:
            features = self.preprocess_logs(current_logs)
            predictions = self.model.predict(features)
            scores = self.model.score_samples(features)
            
            threats = []
            for i, (pred, score) in enumerate(zip(predictions, scores)):
                if pred == -1:  # Anomaly detected
                    threat = {
                        'timestamp': datetime.now().isoformat(),
                        'log_data': current_logs[i],
                        'anomaly_score': float(score),
                        'severity': 'HIGH' if score < -0.5 else 'MEDIUM'
                    }
                    threats.append(threat)
                    self.logger.warning(f"Threat detected: {json.dumps(threat)}")
            
            return threats
        except Exception as e:
            self.logger.error(f"Error detecting threats: {str(e)}")
            raise

    def analyze_threat(self, threat_data):
        """Analyze a detected threat and provide recommendations."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'threat_data': threat_data,
            'recommendations': [],
            'risk_level': 'HIGH' if threat_data['anomaly_score'] < -0.5 else 'MEDIUM'
        }

        # Add basic recommendations based on threat characteristics
        if threat_data['log_data'].get('error_count', 0) > 10:
            analysis['recommendations'].append(
                "High error rate detected. Check application logs for errors."
            )
        if threat_data['log_data'].get('response_time', 0) > 1000:
            analysis['recommendations'].append(
                "Slow response time detected. Investigate performance issues."
            )

        return analysis

if __name__ == "__main__":
    # Example usage
    detector = ThreatDetector()
    
    # Sample historical logs for training
    historical_logs = [
        {'request_count': 10, 'error_count': 1, 'response_time': 100, 'payload_size': 1024},
        {'request_count': 15, 'error_count': 2, 'response_time': 150, 'payload_size': 2048},
        # Add more historical logs...
    ]
    
    # Train the model
    detector.train(historical_logs)
    
    # Sample current logs for threat detection
    current_logs = [
        {'request_count': 1000, 'error_count': 50, 'response_time': 2000, 'payload_size': 5120},
        {'request_count': 20, 'error_count': 1, 'response_time': 120, 'payload_size': 1536},
    ]
    
    # Detect threats
    threats = detector.detect_threats(current_logs)
    
    # Analyze threats
    for threat in threats:
        analysis = detector.analyze_threat(threat)
        print(json.dumps(analysis, indent=2)) 