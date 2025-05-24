from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from typing import Dict, List
import os
from dotenv import load_dotenv
import sys

# Add parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai.threat_detection import ThreatDetector

# Load environment variables
load_dotenv()

app = FastAPI(title="SecureVision API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Initialize threat detector
threat_detector = ThreatDetector()

@app.get("/")
async def root():
    return {"message": "Welcome to SecureVision API"}

@app.get("/api/security/metrics")
async def get_security_metrics():
    """Get current security metrics."""
    try:
        # Example metrics
        metrics = {
            "threats": 5,
            "vulnerabilities": 12,
            "incidents": 3,
            "compliance": 85
        }
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/security/threats")
async def get_threats():
    """Get current threat analysis."""
    try:
        # Example metrics for threat detection
        metrics = {
            "request_rate": 100,
            "error_rate": 0.05,
            "response_time": 200,
            "payload_size": 1024,
            "unique_ips": 50,
            "auth_failures": 3
        }
        
        # Get threat analysis
        analysis = threat_detector.detect_threats(metrics)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/security/timeline")
async def get_threat_timeline():
    """Get threat timeline data."""
    try:
        # Example timeline data
        timeline = [
            {
                "time": (datetime.now() - timedelta(hours=i)).isoformat(),
                "threats": i % 5 + 1
            }
            for i in range(24)
        ]
        return timeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/security/vulnerabilities")
async def get_vulnerabilities():
    """Get vulnerability distribution data."""
    try:
        # Example vulnerability data
        vulnerabilities = [
            {"name": "SQL Injection", "value": 30},
            {"name": "XSS", "value": 25},
            {"name": "CSRF", "value": 20},
            {"name": "Authentication", "value": 15},
            {"name": "Authorization", "value": 10}
        ]
        return vulnerabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 