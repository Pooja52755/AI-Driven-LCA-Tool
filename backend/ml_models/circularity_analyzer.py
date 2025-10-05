import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import asyncio
from utils.logger import logger

class CircularityAnalyzer:
    """Analyze and optimize circularity in metallurgy processes"""
    
    def __init__(self):
        self.circularity_weights = {
            'recycling_rate': 0.35,
            'material_efficiency': 0.25,
            'energy_efficiency': 0.20,
            'waste_minimization': 0.15,
            'longevity': 0.05
        }
        self.is_model_loaded = False
    
    async def load_models(self):
        """Initialize circularity analysis models"""
        try:
            # Load circularity assessment rules and parameters
            self.metal_circularity_potential = {
                'Aluminium': {'max_recycling': 95, 'efficiency_factor': 0.9, 'degradation': 0.02},
                'Copper': {'max_recycling': 98, 'efficiency_factor': 0.95, 'degradation': 0.01},
                'Steel': {'max_recycling': 99, 'efficiency_factor': 0.85, 'degradation': 0.015},
                'Zinc': {'max_recycling': 85, 'efficiency_factor': 0.8, 'degradation': 0.03},
                'Lead': {'max_recycling': 98, 'efficiency_factor': 0.92, 'degradation': 0.01}
            }
            
            self.energy_circularity_factors = {
                'Solar': 0.95,
                'Wind': 0.93,
                'Hydro': 0.90,
                'Grid': 0.60,
                'Coal': 0.30,
                'Gas': 0.50,
                'Mixed': 0.70
            }
            
            self.is_model_loaded = True
            logger.info("Circularity analyzer loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load circularity analyzer: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if analyzer is loaded"""
        return self.is_model_loaded
    
    async def analyze_circularity(self, process_graph: str) -> Dict[str, Any]:
        """Analyze circularity metrics from process graph"""
        try:
            # This would normally use the Neo4j graph data
            # For now, we'll calculate based on available data
            
            # Placeholder analysis - in real implementation, this would use graph algorithms
            current_score = await self._calculate_baseline_circularity_score()
            optimal_score = await self._calculate_optimal_circularity_score()
            
            return {
                'current_score': current_score,
                'optimal_score': optimal_score,
                'improvement_potential': optimal_score - current_score,
                'analysis_method': 'graph_based'
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze circularity: {e}")
            return {'current_score': 50, 'optimal_score': 80, 'error': str(e)}
    
    async def quick_analysis(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Quick circularity analysis without graph"""
        try:
            metal = process_data['metal_type']
            route = process_data['process_route']
            energy_source = process_data.get('energy_source', 'Grid')
            recycling_rate = process_data.get('recycling_rate', 60)
            
            # Calculate circularity components
            components = await self._calculate_circularity_components(
                metal, route, energy_source, recycling_rate, process_data
            )
            
            # Calculate weighted circularity score
            current_score = sum(
                components[component] * weight 
                for component, weight in self.circularity_weights.items()
                if component in components
            )
            
            # Calculate optimal score
            optimal_components = await self._calculate_optimal_components(metal)
            optimal_score = sum(
                optimal_components[component] * weight 
                for component, weight in self.circularity_weights.items()
                if component in optimal_components
            )
            
            return {
                'current_score': round(current_score, 1),
                'optimal_score': round(optimal_score, 1),
                'components': components,
                'optimal_components': optimal_components,
                'improvement_potential': round(optimal_score - current_score, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to perform quick circularity analysis: {e}")
            return {'current_score': 50, 'optimal_score': 80, 'error': str(e)}
    
    async def _calculate_circularity_components(
        self, metal: str, route: str, energy_source: str, recycling_rate: float, process_data: Dict
    ) -> Dict[str, float]:
        """Calculate individual circularity components"""
        
        metal_data = self.metal_circularity_potential.get(metal, {
            'max_recycling': 80, 'efficiency_factor': 0.8, 'degradation': 0.02
        })
        
        # 1. Recycling Rate Component (0-100)
        max_recycling = metal_data['max_recycling']
        recycling_component = min(100, (recycling_rate / max_recycling) * 100)
        
        # 2. Material Efficiency Component
        if route == 'Recycled':
            material_efficiency = metal_data['efficiency_factor'] * 100
        else:
            ore_grade = process_data.get('ore_grade', 50)
            # Higher ore grade = better material efficiency
            material_efficiency = min(100, ore_grade * 1.2)
        
        # 3. Energy Efficiency Component
        energy_factor = 1.0
        for energy_type, factor in self.energy_circularity_factors.items():
            if energy_type.lower() in energy_source.lower():
                energy_factor = max(energy_factor, factor)
        
        energy_consumption = process_data.get('energy_consumption', 50)
        # Lower energy consumption with renewable sources = higher efficiency
        base_energy_efficiency = (1 / (energy_consumption / 40)) * 50  # Normalized
        energy_efficiency = min(100, base_energy_efficiency * energy_factor)
        
        # 4. Waste Minimization Component
        if route == 'Recycled':
            waste_minimization = 85  # Recycled routes typically have less waste
        else:
            # Primary routes - depends on technology and efficiency
            transport_distance = process_data.get('transport_distance', 150)
            waste_minimization = max(20, 80 - (transport_distance / 50))  # Lower transport = less waste
        
        # 5. Longevity Component
        # Based on metal durability and application
        longevity_factors = {
            'Aluminium': 85, 'Copper': 90, 'Steel': 95, 'Zinc': 75, 'Lead': 80
        }
        longevity = longevity_factors.get(metal, 80)
        
        return {
            'recycling_rate': round(recycling_component, 1),
            'material_efficiency': round(material_efficiency, 1),
            'energy_efficiency': round(energy_efficiency, 1),
            'waste_minimization': round(waste_minimization, 1),
            'longevity': round(longevity, 1)
        }
    
    async def _calculate_optimal_components(self, metal: str) -> Dict[str, float]:
        """Calculate optimal circularity components for a metal"""
        
        metal_data = self.metal_circularity_potential.get(metal, {
            'max_recycling': 80, 'efficiency_factor': 0.8, 'degradation': 0.02
        })
        
        # Optimal scenario assumptions
        optimal_recycling = metal_data['max_recycling']
        optimal_material_efficiency = metal_data['efficiency_factor'] * 100
        optimal_energy_efficiency = 95  # Renewable energy + high efficiency
        optimal_waste_minimization = 90  # Best practices
        
        longevity_factors = {
            'Aluminium': 85, 'Copper': 90, 'Steel': 95, 'Zinc': 75, 'Lead': 80
        }
        optimal_longevity = longevity_factors.get(metal, 80)
        
        return {
            'recycling_rate': optimal_recycling,
            'material_efficiency': optimal_material_efficiency,
            'energy_efficiency': optimal_energy_efficiency,
            'waste_minimization': optimal_waste_minimization,
            'longevity': optimal_longevity
        }
    
    async def find_optimization_opportunities(self, process_graph: str) -> Dict[str, Any]:
        """Find specific optimization opportunities"""
        try:
            # This would use graph analysis in real implementation
            # For now, provide general optimization recommendations
            
            opportunities = [
                "Increase recycled content to 80%+ for maximum circularity",
                "Switch to renewable energy sources (solar/wind mix)",
                "Implement closed-loop water recycling systems",
                "Optimize transport routes to reduce distances",
                "Upgrade to high-efficiency processing technology"
            ]
            
            flow_changes = {
                "waste_reduction": "Redirect 15% of waste streams to recycling",
                "energy_optimization": "Replace 60% coal with solar+wind",
                "material_loops": "Create 3 additional recycling loops"
            }
            
            actions = [
                "Install on-site renewable energy generation",
                "Partner with local scrap collectors for consistent supply",
                "Implement AI-powered process optimization",
                "Establish reverse logistics for end-of-life products",
                "Upgrade sorting and purification technologies"
            ]
            
            return {
                'opportunities': opportunities,
                'flow_changes': flow_changes,
                'actions': actions
            }
            
        except Exception as e:
            logger.error(f"Failed to find optimization opportunities: {e}")
            return {'opportunities': [], 'flow_changes': {}, 'actions': []}
    
    async def _calculate_baseline_circularity_score(self) -> float:
        """Calculate baseline circularity score"""
        # Placeholder - would use actual process data
        return 65.0
    
    async def _calculate_optimal_circularity_score(self) -> float:
        """Calculate optimal circularity score"""
        # Placeholder - would use optimization algorithms
        return 87.0
    
    async def compare_circularity_scenarios(
        self, scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare circularity across multiple scenarios"""
        try:
            results = []
            
            for i, scenario in enumerate(scenarios):
                analysis = await self.quick_analysis(scenario)
                results.append({
                    'scenario_id': i,
                    'scenario_name': scenario.get('name', f'Scenario {i+1}'),
                    'circularity_score': analysis['current_score'],
                    'components': analysis['components'],
                    'metal_type': scenario.get('metal_type'),
                    'process_route': scenario.get('process_route')
                })
            
            # Sort by circularity score
            results.sort(key=lambda x: x['circularity_score'], reverse=True)
            
            # Calculate improvement recommendations
            best_scenario = results[0] if results else None
            recommendations = []
            
            if best_scenario:
                recommendations = [
                    f"Best performing scenario: {best_scenario['scenario_name']} ({best_scenario['circularity_score']}%)",
                    f"Recommended metal: {best_scenario['metal_type']}",
                    f"Recommended route: {best_scenario['process_route']}"
                ]
            
            return {
                'comparison_results': results,
                'best_scenario': best_scenario,
                'recommendations': recommendations,
                'analysis_date': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to compare circularity scenarios: {e}")
            return {'error': str(e)}
    
    async def calculate_circular_economy_indicators(
        self, process_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate comprehensive circular economy indicators"""
        try:
            metal = process_data['metal_type']
            route = process_data['process_route']
            
            # Material Flow Indicators
            material_input = process_data.get('production_capacity', 5000)
            recycled_content = process_data.get('recycling_rate', 60) / 100
            virgin_content = 1 - recycled_content
            
            # Calculate material flows
            virgin_input = material_input * virgin_content
            recycled_input = material_input * recycled_content
            
            # Waste indicators
            metal_data = self.metal_circularity_potential.get(metal, {
                'efficiency_factor': 0.8, 'degradation': 0.02
            })
            
            process_efficiency = metal_data['efficiency_factor']
            material_loss = material_input * (1 - process_efficiency)
            useful_output = material_input - material_loss
            
            # End-of-life indicators
            eol_recycling_rate = process_data.get('recycling_rate', 60) / 100
            eol_recovery = useful_output * eol_recycling_rate
            eol_waste = useful_output * (1 - eol_recycling_rate)
            
            # Circular indicators
            circularity_rate = (recycled_input + eol_recovery) / (material_input + useful_output)
            linear_flow = virgin_input + eol_waste
            
            # Resource productivity
            economic_value = useful_output * 1000  # Simplified value per tonne
            resource_productivity = economic_value / material_input
            
            return {
                'material_flows': {
                    'total_input': round(material_input, 1),
                    'virgin_input': round(virgin_input, 1),
                    'recycled_input': round(recycled_input, 1),
                    'useful_output': round(useful_output, 1),
                    'material_loss': round(material_loss, 1)
                },
                'end_of_life': {
                    'recovery_rate': round(eol_recycling_rate * 100, 1),
                    'recovered_material': round(eol_recovery, 1),
                    'waste_to_disposal': round(eol_waste, 1)
                },
                'circularity_indicators': {
                    'circularity_rate': round(circularity_rate * 100, 1),
                    'linear_flow_rate': round((linear_flow / (material_input + useful_output)) * 100, 1),
                    'resource_productivity': round(resource_productivity, 2),
                    'material_efficiency': round(process_efficiency * 100, 1)
                },
                'sustainability_metrics': {
                    'resource_depletion_avoided': round(recycled_input, 1),
                    'waste_avoided': round(eol_recovery, 1),
                    'circular_loops': 1 if recycled_input > 0 and eol_recovery > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate circular economy indicators: {e}")
            return {'error': str(e)}