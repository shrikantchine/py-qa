"""
Main entry point for the project
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
