#!/usr/bin/env python3
"""
Minimal LCA Tool API server - Synchronous version for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Driven LCA Tool for Metallurgy",
    description="Life Cycle Assessment tool for metallurgical processes",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MetalProcessInput(BaseModel):
    metal_type: str
    process_route: str
    production_capacity: float
    energy_source: str
    processing_location: str
    ore_grade: Optional[float] = None
    end_of_life_option: str = "Recycling"
    recycling_rate: Optional[float] = None
    energy_consumption: Optional[float] = None
    transport_distance: Optional[float] = None

# Global storage for comparison data
stored_analyses = []

# Mock functions (synchronous)
def calculate_lca_metrics(data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate LCA metrics"""
    metal_type = data.get('metal_type', 'Aluminium')
    capacity = data.get('production_capacity', 1000)
    
    # Base emissions for different metals
    base_values = {
        'Aluminium': {'energy': 15.2, 'co2': 12.5},
        'Copper': {'energy': 12.8, 'co2': 8.2},
        'Steel': {'energy': 20.1, 'co2': 2.8},
        'Zinc': {'energy': 14.5, 'co2': 6.1},
        'Lead': {'energy': 11.2, 'co2': 4.3}
    }
    
    base = base_values.get(metal_type, base_values['Aluminium'])
    capacity_factor = capacity / 1000.0
    
    return {
        'energy_consumption': round(base['energy'] * capacity_factor, 2),
        'co2_emissions': round(base['co2'] * capacity_factor, 2),
        'water_usage': round(150 * capacity_factor, 2),
        'waste_generation': round(15 * capacity_factor, 2),
        'circularity_score': 85.0,
        'recycled_content': 75.0,
        'resource_efficiency': 80.0
    }

# API Routes
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "API is running normally"
    }

@app.post("/api/lca/analyze")
def analyze_lca(process_input: MetalProcessInput):
    """Analyze LCA for a metal process"""
    try:
        # Convert to dict for processing
        data = process_input.model_dump()
        
        # Calculate metrics
        metrics = calculate_lca_metrics(data)
        
        # Create result
        result = {
            "metal_type": data["metal_type"],
            "process_route": data["process_route"],
            "energy_consumption": metrics["energy_consumption"],
            "co2_emissions": metrics["co2_emissions"],
            "water_usage": metrics["water_usage"],
            "waste_generation": metrics["waste_generation"],
            "circularity_score": metrics["circularity_score"],
            "recycled_content": metrics["recycled_content"],
            "resource_efficiency": metrics["resource_efficiency"],
            "predicted_values": {
                "confidence": 0.95,
                "model_version": "1.0"
            },
            "confidence_scores": {
                "energy": 0.92,
                "emissions": 0.88,
                "water": 0.85
            }
        }
        
        # Store for comparison
        stored_analyses.append({
            "id": len(stored_analyses) + 1,
            "timestamp": "2024-01-01T00:00:00Z",
            "input": data,
            "results": result
        })
        
        return result
        
    except Exception as e:
        logger.error(f"LCA analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comparisons")
def get_stored_comparisons():
    """Get stored analyses for comparison"""
    return {
        "analyses": stored_analyses,
        "comparison_available": len(stored_analyses) >= 2,
        "total_count": len(stored_analyses)
    }

@app.delete("/api/comparisons")
def clear_stored_comparisons():
    """Clear all stored comparisons"""
    global stored_analyses
    stored_analyses = []
    return {"message": "All stored comparisons cleared"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple LCA Tool API")
    print("📊 Server: http://localhost:8000")
    print("⚡ Press CTRL+C to stop")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")