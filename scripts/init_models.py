import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.threat_detection import ThreatDetector

def generate_sample_data(n_samples=1000):
    """Generate sample data for model training."""
    np.random.seed(42)
    
    # Generate timestamps
    base_time = datetime.now() - timedelta(days=30)
    timestamps = [base_time + timedelta(hours=i) for i in range(n_samples)]
    
    # Generate normal metrics
    data = {
        'timestamp': timestamps,
        'request_rate': np.random.normal(100, 20, n_samples),
        'error_rate': np.random.normal(0.05, 0.02, n_samples),
        'response_time': np.random.normal(200, 50, n_samples),
        'payload_size': np.random.normal(1024, 200, n_samples),
        'unique_ips': np.random.normal(50, 10, n_samples),
        'auth_failures': np.random.normal(2, 1, n_samples)
    }
    
    # Add some anomalies
    anomaly_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
    for idx in anomaly_indices:
        data['request_rate'][idx] *= 3
        data['error_rate'][idx] *= 4
        data['auth_failures'][idx] *= 5
    
    return pd.DataFrame(data)

def init_models():
    """Initialize and train ML models."""
    try:
        # Create models directory if it doesn't exist
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # Initialize threat detector
        detector = ThreatDetector()
        
        # Generate and prepare training data
        print("Generating training data...")
        training_data = generate_sample_data()
        
        # Train the model
        print("Training threat detection model...")
        result = detector.train_model(training_data.to_dict('records'))
        
        if result['status'] == 'success':
            print("Model training completed successfully!")
            print(f"Model saved to: {os.path.abspath('models/threat_detection_model.joblib')}")
        else:
            print(f"Error training model: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        raise

if __name__ == "__main__":
    init_models() 