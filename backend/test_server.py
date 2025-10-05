#!/usr/bin/env python3
"""Test minimal FastAPI server"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("Starting minimal test server...")
    uvicorn.run(app, host="127.0.0.1", port=8004)