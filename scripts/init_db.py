from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

def init_database():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "securevision")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "securevision123")
    
    # Create database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create tables
        with engine.connect() as connection:
            # Create security_metrics table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS security_metrics (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    threat_score FLOAT,
                    threat_level VARCHAR(20),
                    is_anomaly BOOLEAN,
                    confidence FLOAT,
                    metrics JSONB
                )
            """))
            
            # Create security_incidents table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS security_incidents (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    incident_type VARCHAR(50),
                    severity VARCHAR(20),
                    description TEXT,
                    status VARCHAR(20),
                    resolution TEXT
                )
            """))
            
            # Create users table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    hashed_password VARCHAR(200) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create audit_logs table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER REFERENCES users(id),
                    action VARCHAR(50),
                    details JSONB
                )
            """))
            
            print("Database tables created successfully!")
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_database() 