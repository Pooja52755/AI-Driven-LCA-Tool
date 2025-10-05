#!/usr/bin/env python3
"""
Minimal LCA Tool API server for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
import logging
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Driven LCA Tool for Metallurgy",
    description="Life Cycle Assessment tool for metallurgical processes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

class LCAResult(BaseModel):
    metal_type: str
    process_route: str
    energy_consumption: float
    co2_emissions: float
    water_usage: float
    waste_generation: float
    land_use: Optional[float] = None
    gwp: Optional[float] = None
    acidification_potential: Optional[float] = None
    eutrophication_potential: Optional[float] = None
    human_toxicity: Optional[float] = None
    circularity_score: float
    recycled_content: float
    resource_efficiency: float
    predicted_values: Dict[str, Any]
    confidence_scores: Dict[str, float]

class ModelMetrics(BaseModel):
    r2_score: float
    f1_score: float
    accuracy: float
    mae: float
    rmse: float

class CircularityAnalysis(BaseModel):
    current_score: float
    optimal_score: float
    improvement_opportunities: List[str]
    flow_optimization: Dict[str, Any]
    recommended_actions: List[str]

# Global storage for comparison data (in a real app, this would be in a database)
stored_analyses = []

# Mock ML functions
async def calculate_lca_metrics(data: Dict[str, Any]) -> Dict[str, float]:
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
        'land_use': round(1.2 * capacity_factor, 2),
        'acidification_potential': round(0.3 * capacity_factor, 3),
        'eutrophication_potential': round(0.2 * capacity_factor, 3),
        'human_toxicity': round(2.5 * capacity_factor, 2)
    }

async def analyze_circularity(data: Dict[str, Any]) -> Dict[str, float]:
    """Analyze circularity"""
    metal_type = data.get('metal_type', 'Aluminium')
    process_route = data.get('process_route', 'Primary')
    recycling_rate = data.get('recycling_rate', 0.75)
    
    # Base circularity scores by metal type
    base_scores = {
        'Aluminium': 85.0,
        'Copper': 80.0,
        'Steel': 75.0,
        'Zinc': 70.0,
        'Lead': 65.0
    }
    
    base_score = base_scores.get(metal_type, 75.0)
    
    # Adjust for process route
    if process_route == 'Recycled':
        base_score += 10.0  # Bonus for recycled processes
    
    # Adjust for recycling rate
    if recycling_rate:
        base_score = base_score * (0.7 + 0.3 * recycling_rate)
    
    return {
        'overall_score': round(min(95.0, base_score), 1),
        'material_recovery_rate': round(min(95.0, base_score * 0.9), 1),
        'recycling_efficiency': round(min(95.0, base_score * 0.95), 1)
    }

# API Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "neo4j": False,
            "sqlite": True,
            "ml_models": True
        }
    }

@app.get("/api/model/metrics", response_model=ModelMetrics)
async def get_model_metrics():
    """Get AI model performance metrics"""
    return ModelMetrics(
        r2_score=0.89,
        f1_score=0.91,
        accuracy=0.898,
        mae=2.1,
        rmse=3.8
    )

@app.post("/api/lca/analyze", response_model=LCAResult)
async def analyze_lca(process_input: MetalProcessInput):
    """Perform LCA analysis"""
    try:
        # Calculate LCA metrics
        lca_results = await calculate_lca_metrics(process_input.model_dump())
        circularity_data = await analyze_circularity(process_input.model_dump())
        
        # Create response
        result = LCAResult(
            metal_type=process_input.metal_type,
            process_route=process_input.process_route,
            energy_consumption=lca_results['energy_consumption'],
            co2_emissions=lca_results['co2_emissions'],
            water_usage=lca_results['water_usage'],
            waste_generation=lca_results['waste_generation'],
            land_use=lca_results['land_use'],
            gwp=lca_results['co2_emissions'] * 1000,
            acidification_potential=lca_results['acidification_potential'],
            eutrophication_potential=lca_results['eutrophication_potential'],
            human_toxicity=lca_results['human_toxicity'],
            circularity_score=circularity_data['overall_score'],
            recycled_content=circularity_data['material_recovery_rate'],
            resource_efficiency=circularity_data['recycling_efficiency'],
            predicted_values={
                'temperature': 850.0,
                'pressure': 1.5,
                'efficiency': 85.0
            },
            confidence_scores={
                'energy_consumption': 0.89,
                'co2_emissions': 0.94,
                'water_usage': 0.87,
                'waste_generation': 0.82
            }
        )
        
        # Store analysis for comparison (add to global storage)
        analysis_record = {
            "id": len(stored_analyses) + 1,
            "timestamp": "2025-10-05T12:00:00Z",
            "input": process_input.model_dump(),
            "result": result.model_dump(),
            "scenario_name": f"{process_input.metal_type} - {process_input.process_route}"
        }
        stored_analyses.append(analysis_record)
        logger.info(f"Stored analysis #{len(stored_analyses)}: {analysis_record['scenario_name']}")
        
        return result
        
    except Exception as e:
        logger.error(f"LCA analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/circularity/analyze", response_model=CircularityAnalysis)
async def analyze_circularity_endpoint(process_input: MetalProcessInput):
    """Analyze circularity potential and optimization opportunities"""
    try:
        # Calculate circularity metrics
        circularity_data = await analyze_circularity(process_input.model_dump())
        
        # Enhanced circularity analysis with recommendations
        metal_type = process_input.metal_type
        process_route = process_input.process_route
        
        # Generate improvement opportunities based on metal type and process
        improvement_opportunities = [
            f"Optimize {metal_type.lower()} recycling efficiency",
            "Implement closed-loop material flow systems",
            "Enhance energy recovery from waste heat",
            "Develop advanced sorting technologies"
        ]
        
        if process_route == "Primary":
            improvement_opportunities.extend([
                "Consider transition to recycled feedstock",
                "Implement by-product utilization strategies"
            ])
        
        # Flow optimization recommendations
        flow_optimization = {
            "material_efficiency": {
                "current": circularity_data['material_recovery_rate'],
                "target": min(95.0, circularity_data['material_recovery_rate'] + 15),
                "strategies": ["Advanced separation", "Quality control"]
            },
            "energy_efficiency": {
                "current": 75.0,
                "target": 85.0,
                "strategies": ["Heat recovery", "Process optimization"]
            }
        }
        
        # Recommended actions
        recommended_actions = [
            "Implement digital tracking for material flows",
            f"Upgrade {metal_type.lower()} processing equipment",
            "Establish partnerships with recycling facilities",
            "Invest in renewable energy sources",
            "Develop circular business models"
        ]
        
        result = CircularityAnalysis(
            current_score=circularity_data['overall_score'],
            optimal_score=min(95.0, circularity_data['overall_score'] + 20),
            improvement_opportunities=improvement_opportunities,
            flow_optimization=flow_optimization,
            recommended_actions=recommended_actions
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Circularity analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare")
async def compare_processes(processes: List[MetalProcessInput]):
    """Compare multiple metal processing scenarios"""
    try:
        comparison_results = []
        
        for i, process in enumerate(processes):
            # Calculate LCA metrics for each process
            lca_results = await calculate_lca_metrics(process.model_dump())
            circularity_data = await analyze_circularity(process.model_dump())
            
            # Create comparison entry
            process_result = {
                "scenario_name": f"{process.metal_type} - {process.process_route}",
                "metal_type": process.metal_type,
                "process_route": process.process_route,
                "production_capacity": process.production_capacity,
                "energy_source": process.energy_source,
                "lca_results": {
                    "energy_consumption": lca_results['energy_consumption'],
                    "co2_emissions": lca_results['co2_emissions'],
                    "water_usage": lca_results['water_usage'],
                    "waste_generation": lca_results['waste_generation']
                },
                "circularity_score": circularity_data['overall_score'],
                "environmental_impact_score": round(
                    100 - (lca_results['co2_emissions'] / 20 * 100), 1
                ),  # Simple scoring: lower emissions = higher score
                "sustainability_rating": round(
                    (circularity_data['overall_score'] + 
                     (100 - lca_results['co2_emissions'] / 20 * 100)) / 2, 1
                )
            }
            
            comparison_results.append(process_result)
        
        # Find best scenario based on sustainability rating
        best_scenario = max(comparison_results, 
                           key=lambda x: x['sustainability_rating'])
        
        # Calculate summary statistics
        avg_co2 = sum(r['lca_results']['co2_emissions'] for r in comparison_results) / len(comparison_results)
        avg_circularity = sum(r['circularity_score'] for r in comparison_results) / len(comparison_results)
        
        response = {
            "scenarios": comparison_results,
            "summary": {
                "total_scenarios": len(comparison_results),
                "best_scenario": best_scenario['scenario_name'],
                "best_sustainability_rating": best_scenario['sustainability_rating'],
                "average_co2_emissions": round(avg_co2, 2),
                "average_circularity_score": round(avg_circularity, 1),
                "improvement_potential": round(
                    best_scenario['sustainability_rating'] - 
                    min(r['sustainability_rating'] for r in comparison_results), 1
                )
            },
            "recommendations": [
                f"Adopt {best_scenario['metal_type'].lower()} processing approach",
                f"Focus on {best_scenario['process_route'].lower()} route optimization",
                "Implement energy-efficient technologies",
                "Enhance circular economy practices"
            ]
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Process comparison failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comparisons")
async def get_stored_comparisons():
    """Get all stored analyses for comparison"""
    try:
        logger.info(f"Retrieving stored comparisons: {len(stored_analyses)} analyses available")
        if len(stored_analyses) < 2:
            return {
                "message": "Add multiple processes from the Input tab to compare their environmental impacts.",
                "analyses": stored_analyses,
                "comparison_available": False
            }
        
        # Generate comparison from stored analyses
        comparison_results = []
        
        for analysis in stored_analyses:
            result = analysis["result"]
            comparison_results.append({
                "scenario_name": analysis["scenario_name"],
                "metal_type": result["metal_type"],
                "process_route": result["process_route"],
                "lca_results": {
                    "energy_consumption": result["energy_consumption"],
                    "co2_emissions": result["co2_emissions"],
                    "water_usage": result["water_usage"],
                    "waste_generation": result["waste_generation"]
                },
                "circularity_score": result["circularity_score"],
                "environmental_impact_score": round(100 - (result["co2_emissions"] / 20 * 100), 1),
                "sustainability_rating": round((result["circularity_score"] + (100 - result["co2_emissions"] / 20 * 100)) / 2, 1)
            })
        
        # Find best scenario
        best_scenario = max(comparison_results, key=lambda x: x['sustainability_rating'])
        
        return {
            "scenarios": comparison_results,
            "summary": {
                "total_scenarios": len(comparison_results),
                "best_scenario": best_scenario['scenario_name'],
                "best_sustainability_rating": best_scenario['sustainability_rating']
            },
            "comparison_available": True
        }
        
    except Exception as e:
        logger.error(f"Failed to get comparisons: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test/populate")
async def populate_test_data():
    """Populate test data for debugging comparison functionality"""
    global stored_analyses
    
    # Clear existing data
    stored_analyses = []
    
    # Add test analysis 1
    test_analysis_1 = {
        "id": 1,
        "timestamp": "2025-10-05T12:00:00Z",
        "input": {"metal_type": "Copper", "process_route": "Recycled", "production_capacity": 5000},
        "result": {
            "metal_type": "Copper",
            "process_route": "Recycled", 
            "energy_consumption": 64.0,
            "co2_emissions": 41.0,
            "water_usage": 750.0,
            "waste_generation": 75.0,
            "circularity_score": 95.0,
            "recycled_content": 85.0,
            "resource_efficiency": 90.0
        },
        "scenario_name": "Copper - Recycled"
    }
    
    # Add test analysis 2
    test_analysis_2 = {
        "id": 2,
        "timestamp": "2025-10-05T12:05:00Z",
        "input": {"metal_type": "Lead", "process_route": "Recycled", "production_capacity": 3000},
        "result": {
            "metal_type": "Lead",
            "process_route": "Recycled",
            "energy_consumption": 33.6,
            "co2_emissions": 12.9,
            "water_usage": 450.0,
            "waste_generation": 45.0,
            "circularity_score": 95.0,
            "recycled_content": 80.0,
            "resource_efficiency": 85.0
        },
        "scenario_name": "Lead - Recycled"
    }
    
    stored_analyses.append(test_analysis_1)
    stored_analyses.append(test_analysis_2)
    
    logger.info(f"Populated {len(stored_analyses)} test analyses")
    
    return {
        "message": f"Populated {len(stored_analyses)} test analyses",
        "analyses": stored_analyses
    }

@app.delete("/api/comparisons")
async def clear_stored_comparisons():
    """Clear all stored analyses"""
    global stored_analyses
    stored_analyses = []
    return {"message": "All stored comparisons cleared"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI-Driven LCA Tool API (Minimal Version)")
    print("📊 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("⚡ Press CTRL+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")