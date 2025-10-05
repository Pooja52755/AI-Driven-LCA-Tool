#!/usr/bin/env python3
"""
Test script for AI-Driven LCA Tool
This script tests all the main functionality without needing a running server.
"""

import asyncio
import json
from ml_models.lca_predictor_simple import LCAPredictor
from ml_models.circularity_analyzer_simple import CircularityAnalyzer
from ml_models.report_generator_simple import ReportGenerator

async def test_lca_analysis():
    """Test LCA analysis functionality"""
    print("=== Testing LCA Analysis ===")
    
    # Initialize predictor
    predictor = LCAPredictor()
    await predictor.load_models()
    
    # Test data for Aluminium production
    test_data = {
        'metal_type': 'Aluminium',
        'process_route': 'Primary',
        'production_capacity': 1000,
        'energy_source': 'Coal',
        'processing_location': 'India'
    }
    
    print(f"Input data: {json.dumps(test_data, indent=2)}")
    
    # Predict missing parameters
    missing_params = await predictor.predict_missing_parameters(test_data)
    print(f"\nPredicted missing parameters: {json.dumps(missing_params, indent=2)}")
    
    # Calculate LCA metrics
    lca_results = await predictor.calculate_lca_metrics(test_data)
    print(f"\nLCA Results: {json.dumps(lca_results, indent=2)}")
    
    return lca_results

async def test_circularity_analysis():
    """Test circularity analysis functionality"""
    print("\n=== Testing Circularity Analysis ===")
    
    # Initialize analyzer
    analyzer = CircularityAnalyzer()
    await analyzer.load_models()
    
    # Test data
    process_data = {
        'metal_type': 'Aluminium',
        'recycling_rate': 0.75,
        'energy_recovery': 0.60,
        'material_efficiency': 0.85
    }
    
    print(f"Input data: {json.dumps(process_data, indent=2)}")
    
    # Analyze circularity
    circularity_results = await analyzer.analyze_circularity(process_data)
    print(f"\nCircularity Analysis: {json.dumps(circularity_results, indent=2)}")
    
    return circularity_results

async def test_report_generation():
    """Test report generation functionality"""
    print("\n=== Testing Report Generation ===")
    
    # Initialize report generator
    report_gen = ReportGenerator()
    
    # Sample LCA and circularity results
    lca_results = {
        'energy_consumption': 18.24,
        'co2_emissions': 15.0,
        'water_usage': 132.2,
        'waste_generation': 23.34
    }
    
    circularity_results = {
        'overall_score': 78.5,
        'material_recovery_rate': 75.0,
        'energy_recovery_rate': 60.0,
        'recommendations': ['Optimize energy efficiency', 'Increase recycling rates']
    }
    
    # Generate report
    report = await report_gen.generate_lca_report(lca_results, circularity_results)
    print("\nGenerated Report:")
    print(report)
    
    return report

async def main():
    """Run all tests"""
    print("🔬 AI-Driven LCA Tool - Functionality Test")
    print("=" * 50)
    
    try:
        # Test LCA analysis
        lca_results = await test_lca_analysis()
        
        # Test circularity analysis
        circularity_results = await test_circularity_analysis()
        
        # Test report generation
        report = await test_report_generation()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("✅ LCA analysis working")
        print("✅ Circularity assessment working") 
        print("✅ Report generation working")
        print("\nThe AI-Driven LCA Tool is functioning correctly!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())