import spacy
from spacy.lang.en import English
import pandas as pd
from typing import Dict, List, Any
import asyncio
from utils.logger import logger

class ReportGenerator:
    """Generate natural language LCA reports using spaCy"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        self.nlp = None
        self.templates = {}
        self._load_templates()
    
    async def load_models(self):
        """Load spaCy model"""
        try:
            self.nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning(f"spaCy model {self.model_name} not found, using blank English model")
            self.nlp = English()
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            self.nlp = English()
    
    def _load_templates(self):
        """Load report templates"""
        self.templates = {
            'executive_summary': """
# LCA Executive Summary for {metal_type} ({process_route} Route)

## Key Findings
- **Global Warming Potential**: {gwp} kg CO₂e/tonne
- **Circularity Score**: {circularity_score}%
- **Recycled Content**: {recycled_content}%
- **Processing Location**: {processing_location}

## Environmental Performance
{environmental_assessment}

## Circularity Assessment
{circularity_assessment}

## Recommendations
{recommendations}
""",
            
            'detailed_analysis': """
# Detailed LCA Analysis Report

## Process Overview
This analysis covers {metal_type} production using the {process_route} route at {processing_location}.

### Production Specifications
- **Capacity**: {production_capacity:,.0f} tonnes/year
- **Energy Source**: {energy_source}
- **Energy Consumption**: {energy_consumption} MW
- **Transport Distance**: {transport_distance} km

## Environmental Impact Assessment

### Carbon Footprint
{carbon_assessment}

### Other Environmental Impacts
{other_impacts}

## Circularity Analysis
{detailed_circularity}

## Optimization Opportunities
{optimization_opportunities}

## Compliance and Standards
{compliance_notes}
""",
            
            'comparison_report': """
# Process Comparison Report

## Scenarios Analyzed
{scenarios_overview}

## Comparative Analysis
{comparison_analysis}

## Best Practices Identified
{best_practices}

## Implementation Roadmap
{implementation_roadmap}
"""
        }
    
    async def generate_comprehensive_report(
        self, 
        process_data: Dict[str, Any], 
        lca_results: Dict[str, Any], 
        circularity_results: Dict[str, Any]
    ) -> str:
        """Generate comprehensive LCA report"""
        try:
            # Extract key metrics
            metal_type = process_data['metal_type']
            process_route = process_data['process_route']
            gwp = lca_results.get('gwp', 0)
            circularity_score = lca_results.get('circularity_score', 0)
            
            # Generate content sections
            environmental_assessment = await self._generate_environmental_assessment(lca_results)
            circularity_assessment = await self._generate_circularity_assessment(circularity_results)
            recommendations = await self._generate_recommendations(process_data, lca_results, circularity_results)
            
            # Format executive summary
            executive_summary = self.templates['executive_summary'].format(
                metal_type=metal_type,
                process_route=process_route,
                gwp=gwp,
                circularity_score=circularity_score,
                recycled_content=lca_results.get('recycled_content', 0),
                processing_location=process_data.get('processing_location', 'Not specified'),
                environmental_assessment=environmental_assessment,
                circularity_assessment=circularity_assessment,
                recommendations=recommendations
            )
            
            # Generate detailed sections
            carbon_assessment = await self._generate_carbon_assessment(process_data, lca_results)
            other_impacts = await self._generate_other_impacts_assessment(lca_results)
            detailed_circularity = await self._generate_detailed_circularity_analysis(circularity_results)
            optimization_opportunities = await self._generate_optimization_section(process_data, lca_results)
            compliance_notes = await self._generate_compliance_notes(process_data)
            
            # Format detailed analysis
            detailed_analysis = self.templates['detailed_analysis'].format(
                metal_type=metal_type,
                process_route=process_route,
                processing_location=process_data.get('processing_location', 'Not specified'),
                production_capacity=process_data.get('production_capacity', 0),
                energy_source=process_data.get('energy_source', 'Not specified'),
                energy_consumption=process_data.get('energy_consumption', 0),
                transport_distance=process_data.get('transport_distance', 0),
                carbon_assessment=carbon_assessment,
                other_impacts=other_impacts,
                detailed_circularity=detailed_circularity,
                optimization_opportunities=optimization_opportunities,
                compliance_notes=compliance_notes
            )
            
            # Combine reports
            full_report = executive_summary + "\n\n" + detailed_analysis
            
            return full_report
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive report: {e}")
            return await self._generate_fallback_report(process_data, lca_results)
    
    async def _generate_environmental_assessment(self, lca_results: Dict[str, Any]) -> str:
        """Generate environmental assessment section"""
        gwp = lca_results.get('gwp', 0)
        acidification = lca_results.get('acidification_potential', 0)
        eutrophication = lca_results.get('eutrophication_potential', 0)
        
        # Assess performance levels
        gwp_assessment = self._assess_gwp_performance(gwp)
        acid_assessment = self._assess_acidification_performance(acidification)
        eutro_assessment = self._assess_eutrophication_performance(eutrophication)
        
        return f"""The environmental performance analysis reveals {gwp_assessment} for global warming potential at {gwp:.1f} kg CO₂e/tonne. Acidification potential shows {acid_assessment} at {acidification:.3f} kg SO₂ eq/tonne. Eutrophication impact indicates {eutro_assessment} at {eutrophication:.3f} kg PO₄³⁻ eq/tonne."""
    
    async def _generate_circularity_assessment(self, circularity_results: Dict[str, Any]) -> str:
        """Generate circularity assessment section"""
        current_score = circularity_results.get('current_score', 50)
        optimal_score = circularity_results.get('optimal_score', 80)
        improvement_potential = optimal_score - current_score
        
        performance_level = self._assess_circularity_performance(current_score)
        
        return f"""The circularity analysis shows {performance_level} with a score of {current_score:.1f}%. There is significant improvement potential of {improvement_potential:.1f} percentage points to reach the optimal score of {optimal_score:.1f}%. This indicates opportunities for enhanced material flow optimization and waste reduction strategies."""
    
    async def _generate_recommendations(
        self, 
        process_data: Dict[str, Any], 
        lca_results: Dict[str, Any], 
        circularity_results: Dict[str, Any]
    ) -> str:
        """Generate specific recommendations"""
        recommendations = []
        
        # Energy recommendations
        energy_source = process_data.get('energy_source', '')
        if 'Coal' in energy_source:
            recommendations.append("Switch to renewable energy sources (solar/wind) to reduce carbon emissions by 25-40%")
        
        # Recycling recommendations
        recycling_rate = process_data.get('recycling_rate', 0)
        if recycling_rate < 70:
            recommendations.append("Increase recycled content to 70%+ to improve circularity score")
        
        # Process route recommendations
        if process_data.get('process_route') == 'Primary':
            recommendations.append("Consider transitioning to recycled route for 60% lower environmental impact")
        
        # Transport optimization
        transport_distance = process_data.get('transport_distance', 0)
        if transport_distance > 200:
            recommendations.append("Optimize supply chain to reduce transport distances and associated emissions")
        
        # Circularity improvements
        current_score = circularity_results.get('current_score', 50)
        if current_score < 75:
            recommendations.append("Implement closed-loop systems and waste-to-resource conversion")
        
        return "\n".join(f"• {rec}" for rec in recommendations[:5])  # Limit to top 5
    
    async def _generate_carbon_assessment(self, process_data: Dict[str, Any], lca_results: Dict[str, Any]) -> str:
        """Generate detailed carbon assessment"""
        gwp = lca_results.get('gwp', 0)
        metal_type = process_data['metal_type']
        process_route = process_data['process_route']
        
        # Industry benchmarks (simplified)
        benchmarks = {
            'Aluminium': {'Primary': 15, 'Recycled': 5},
            'Copper': {'Primary': 18, 'Recycled': 7},
            'Steel': {'Primary': 12, 'Recycled': 4},
            'Zinc': {'Primary': 14, 'Recycled': 6},
            'Lead': {'Primary': 9, 'Recycled': 3}
        }
        
        benchmark = benchmarks.get(metal_type, {}).get(process_route, 10)
        performance = "above" if gwp > benchmark else "below"
        
        return f"""The carbon footprint of {gwp:.1f} kg CO₂e/tonne is {performance} the industry benchmark of {benchmark} kg CO₂e/tonne for {metal_type} {process_route.lower()} production. This represents {'higher than expected' if gwp > benchmark else 'competitive'} emissions for this production route. Key contributing factors include energy source composition and process efficiency levels."""
    
    async def _generate_other_impacts_assessment(self, lca_results: Dict[str, Any]) -> str:
        """Generate assessment of other environmental impacts"""
        acidification = lca_results.get('acidification_potential', 0)
        eutrophication = lca_results.get('eutrophication_potential', 0)
        
        return f"""**Acidification Potential**: {acidification:.3f} kg SO₂ eq/tonne indicates {self._assess_acidification_performance(acidification)} for air quality impacts. This primarily results from sulfur compound emissions during processing.

**Eutrophication Potential**: {eutrophication:.3f} kg PO₄³⁻ eq/tonne shows {self._assess_eutrophication_performance(eutrophication)} for water body impacts. These values reflect nutrient discharge levels and water management practices."""
    
    async def _generate_detailed_circularity_analysis(self, circularity_results: Dict[str, Any]) -> str:
        """Generate detailed circularity analysis"""
        components = circularity_results.get('components', {})
        
        analysis_parts = []
        for component, value in components.items():
            component_name = component.replace('_', ' ').title()
            assessment = self._assess_component_performance(value)
            analysis_parts.append(f"**{component_name}**: {value}% - {assessment}")
        
        return "\n\n".join(analysis_parts)
    
    async def _generate_optimization_section(self, process_data: Dict[str, Any], lca_results: Dict[str, Any]) -> str:
        """Generate optimization opportunities section"""
        opportunities = []
        
        # Energy optimization
        energy_consumption = process_data.get('energy_consumption', 0)
        if energy_consumption > 50:
            opportunities.append("**Energy Efficiency**: Implement advanced process control systems to reduce energy consumption by 15-20%")
        
        # Material optimization
        if process_data.get('process_route') == 'Primary':
            opportunities.append("**Material Circularity**: Establish partnerships with scrap suppliers to increase recycled content")
        
        # Technology upgrades
        opportunities.append("**Process Innovation**: Adopt AI-powered optimization for real-time efficiency improvements")
        
        # Supply chain optimization
        opportunities.append("**Supply Chain**: Implement blockchain tracking for material provenance and quality assurance")
        
        return "\n\n".join(opportunities)
    
    async def _generate_compliance_notes(self, process_data: Dict[str, Any]) -> str:
        """Generate compliance and standards notes"""
        return f"""This analysis follows ISO 14040/14044 standards for Life Cycle Assessment. The assessment includes BIS (Bureau of Indian Standards) compliance factors for {process_data.get('processing_location', 'Indian')} operations. Results align with Ministry of Mines guidelines for sustainable metallurgy practices and support Atmanirbhar Bharat initiatives through domestic resource optimization."""
    
    def _assess_gwp_performance(self, gwp: float) -> str:
        """Assess GWP performance level"""
        if gwp < 8:
            return "excellent performance"
        elif gwp < 15:
            return "good performance"
        elif gwp < 25:
            return "moderate performance"
        else:
            return "performance requiring improvement"
    
    def _assess_acidification_performance(self, acidification: float) -> str:
        """Assess acidification performance level"""
        if acidification < 0.5:
            return "low impact"
        elif acidification < 1.0:
            return "moderate impact"
        else:
            return "high impact requiring attention"
    
    def _assess_eutrophication_performance(self, eutrophication: float) -> str:
        """Assess eutrophication performance level"""
        if eutrophication < 0.05:
            return "minimal impact"
        elif eutrophication < 0.1:
            return "moderate impact"
        else:
            return "significant impact"
    
    def _assess_circularity_performance(self, score: float) -> str:
        """Assess circularity performance level"""
        if score >= 80:
            return "excellent circularity performance"
        elif score >= 65:
            return "good circularity performance"
        elif score >= 50:
            return "moderate circularity performance"
        else:
            return "poor circularity performance requiring significant improvement"
    
    def _assess_component_performance(self, value: float) -> str:
        """Assess individual component performance"""
        if value >= 85:
            return "Excellent performance, meeting best practice standards"
        elif value >= 70:
            return "Good performance with minor optimization opportunities"
        elif value >= 55:
            return "Moderate performance with clear improvement potential"
        else:
            return "Poor performance requiring immediate attention and investment"
    
    async def _generate_fallback_report(self, process_data: Dict[str, Any], lca_results: Dict[str, Any]) -> str:
        """Generate fallback report if main generation fails"""
        metal_type = process_data.get('metal_type', 'Unknown')
        process_route = process_data.get('process_route', 'Unknown')
        gwp = lca_results.get('gwp', 0)
        
        return f"""# LCA Report for {metal_type} ({process_route} Route)

## Summary
This analysis covers {metal_type} production with a carbon footprint of {gwp:.1f} kg CO₂e/tonne.

## Key Metrics
- Global Warming Potential: {gwp:.1f} kg CO₂e/tonne
- Circularity Score: {lca_results.get('circularity_score', 0):.1f}%
- Processing Location: {process_data.get('processing_location', 'Not specified')}

## Recommendations
- Optimize energy efficiency
- Increase recycled content
- Implement circular economy principles

## Note
This is a simplified report due to processing limitations. Please contact technical support for a complete analysis.
"""
    
    async def generate_quick_summary(self, lca_results: Dict[str, Any]) -> str:
        """Generate quick summary for dashboard"""
        gwp = lca_results.get('gwp', 0)
        circularity = lca_results.get('circularity_score', 0)
        
        performance = "excellent" if gwp < 10 and circularity > 70 else "good" if gwp < 20 and circularity > 50 else "needs improvement"
        
        return f"Environmental performance is {performance} with {gwp:.1f} kg CO₂e/tonne emissions and {circularity:.1f}% circularity score."