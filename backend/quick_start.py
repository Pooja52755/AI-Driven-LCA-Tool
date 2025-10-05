#!/usr/bin/env python3
"""
Quick server starter for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    print("Starting server on http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    try:
        uvicorn.run("minimal_server:app", host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")