"""Simplified deployment entry point"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Now import the app
try:
    from backend.app import app
except ImportError:
    # Fallback: try direct import after path manipulation
    os.chdir(str(backend_path))
    from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
