import os
import subprocess
import sys
from pathlib import Path

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        sys.exit(1)

def setup_project():
    # Create necessary directories
    directories = [
        "src/frontend",
        "src/backend",
        "src/ai",
        "src/monitoring",
        "models",
        "logs",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    # Install Python dependencies
    print("Installing Python dependencies...")
    run_command("pip install -r requirements.txt")

    # Install frontend dependencies
    print("Installing frontend dependencies...")
    os.chdir("src/frontend")
    run_command("npm install")
    os.chdir("../..")

    # Initialize database
    print("Initializing database...")
    run_command("python scripts/init_db.py")

    # Initialize ML models
    print("Initializing ML models...")
    run_command("python scripts/init_models.py")

    print("Project setup completed successfully!")

if __name__ == "__main__":
    setup_project() 