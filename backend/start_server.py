#!/usr/bin/env python3
"""
Start the LCA Tool API server
"""

import uvicorn
import sys
import os

if __name__ == "__main__":
    print("Starting AI-Driven LCA Tool API Server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press CTRL+C to stop the server")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to prevent shutdown issues
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)