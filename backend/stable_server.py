#!/usr/bin/env python3
"""
Stable server startup script
"""

import os
import sys

# Ensure we're in the right directory
backend_dir = r"d:\SIH7\ai-lca-metallurgy\backend"
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

print(f"Starting server from: {os.getcwd()}")
print("Available endpoints will be:")
print("  - GET  /api/health")
print("  - GET  /api/model/metrics") 
print("  - POST /api/lca/analyze")
print("  - POST /api/circularity/analyze")
print()

# Import and run
try:
    import uvicorn
    from minimal_server import app
    
    print("🚀 AI-Driven LCA Tool API Server")
    print("📊 http://localhost:8000")
    print("📚 http://localhost:8000/docs")
    print("🔄 Frontend: http://localhost:5000")
    print()
    print("Server starting... Press CTRL+C to stop")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        log_level="info",
        access_log=True
    )
    
except KeyboardInterrupt:
    print("\n✋ Server stopped by user")
except Exception as e:
    print(f"❌ Server error: {e}")
    input("Press Enter to close...")