import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Import the Flask app
from app import app

# This is the entry point for Vercel
if __name__ == "__main__":
    app.run()
