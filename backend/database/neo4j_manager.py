from neo4j import GraphDatabase
from typing import Dict, List, Any, Optional
import json
import asyncio
from utils.logger import logger

class Neo4jManager:
    """Neo4j database manager for process graphs and circularity analysis"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def is_connected(self) -> bool:
        """Check if connected to Neo4j"""
        try:
            with self.driver.session() as session:
                session.run("RETURN 1")
            return True
        except:
            return False
    
    async def create_process_graph(self, process_data: Dict[str, Any]) -> str:
        """Create a process graph for circularity analysis"""
        try:
            with self.driver.session() as session:
                # Create main process node
                process_id = f"{process_data['metal_type']}_{process_data['process_route']}_{hash(str(process_data))}"
                
                # Clear existing graph for this process
                session.run("""
                    MATCH (n {process_id: $process_id})
                    DETACH DELETE n
                """, process_id=process_id)
                
                # Create process nodes and relationships
                if process_data['process_route'] == 'Primary':
                    await self._create_primary_process_graph(session, process_data, process_id)
                else:
                    await self._create_recycled_process_graph(session, process_data, process_id)
                
                logger.info(f"Created process graph: {process_id}")
                return process_id
                
        except Exception as e:
            logger.error(f"Failed to create process graph: {e}")
            raise
    
    async def _create_primary_process_graph(self, session, process_data: Dict, process_id: str):
        """Create graph for primary metal production"""
        metal = process_data['metal_type']
        location = process_data['processing_location']
        
        # Create nodes
        query = """
        CREATE (mine:Mine {
            name: $mine_name,
            location: $location,
            ore_grade: $ore_grade,
            process_id: $process_id
        })
        CREATE (transport1:Transport {
            distance: $transport_distance,
            mode: "truck",
            process_id: $process_id
        })
        CREATE (processing:Processing {
            type: "smelting",
            metal: $metal,
            capacity: $capacity,
            energy_source: $energy_source,
            energy_consumption: $energy_consumption,
            location: $location,
            process_id: $process_id
        })
        CREATE (product:Product {
            metal: $metal,
            route: "primary",
            process_id: $process_id
        })
        CREATE (waste:Waste {
            type: "mining_waste",
            treatment: "landfill",
            process_id: $process_id
        })
        CREATE (eol:EndOfLife {
            option: $eol_option,
            recycling_rate: $recycling_rate,
            process_id: $process_id
        })
        
        // Create relationships
        CREATE (mine)-[:TRANSPORTS]->(transport1)
        CREATE (transport1)-[:DELIVERS_TO]->(processing)
        CREATE (processing)-[:PRODUCES]->(product)
        CREATE (processing)-[:GENERATES]->(waste)
        CREATE (product)-[:ENDS_AS]->(eol)
        """
        
        if process_data.get('recycling_rate', 0) > 0:
            query += """
            CREATE (recycling:Recycling {
                rate: $recycling_rate,
                process_id: $process_id
            })
            CREATE (eol)-[:FEEDS_INTO]->(recycling)
            CREATE (recycling)-[:PRODUCES]->(product)
            """
        
        session.run(query, 
            mine_name=f"{metal}_mine",
            location=location,
            ore_grade=process_data.get('ore_grade', 50),
            transport_distance=process_data.get('transport_distance', 100),
            metal=metal,
            capacity=process_data['production_capacity'],
            energy_source=process_data['energy_source'],
            energy_consumption=process_data.get('energy_consumption', 50),
            eol_option=process_data['end_of_life_option'],
            recycling_rate=process_data.get('recycling_rate', 0),
            process_id=process_id
        )
    
    async def _create_recycled_process_graph(self, session, process_data: Dict, process_id: str):
        """Create graph for recycled metal production"""
        metal = process_data['metal_type']
        location = process_data['processing_location']
        
        query = """
        CREATE (scrap:Scrap {
            metal: $metal,
            quality: "high",
            process_id: $process_id
        })
        CREATE (collection:Collection {
            efficiency: $recycling_rate,
            process_id: $process_id
        })
        CREATE (sorting:Sorting {
            purity: 0.95,
            process_id: $process_id
        })
        CREATE (reprocessing:Reprocessing {
            type: "remelting",
            metal: $metal,
            capacity: $capacity,
            energy_source: $energy_source,
            energy_consumption: $energy_consumption,
            location: $location,
            process_id: $process_id
        })
        CREATE (product:Product {
            metal: $metal,
            route: "recycled",
            quality: "secondary",
            process_id: $process_id
        })
        CREATE (eol:EndOfLife {
            option: $eol_option,
            recycling_rate: $recycling_rate,
            process_id: $process_id
        })
        
        // Create relationships
        CREATE (scrap)-[:COLLECTED_BY]->(collection)
        CREATE (collection)-[:SENDS_TO]->(sorting)
        CREATE (sorting)-[:FEEDS_INTO]->(reprocessing)
        CREATE (reprocessing)-[:PRODUCES]->(product)
        CREATE (product)-[:ENDS_AS]->(eol)
        CREATE (eol)-[:FEEDS_BACK]->(scrap)
        """
        
        session.run(query,
            metal=metal,
            recycling_rate=process_data.get('recycling_rate', 80),
            capacity=process_data['production_capacity'],
            energy_source=process_data['energy_source'],
            energy_consumption=process_data.get('energy_consumption', 30),
            eol_option=process_data['end_of_life_option'],
            process_id=process_id
        )
    
    async def get_process_graph_for_visualization(self, process_id: str) -> Dict[str, Any]:
        """Get process graph data formatted for Vis.js visualization"""
        try:
            with self.driver.session() as session:
                # Get nodes
                nodes_result = session.run("""
                    MATCH (n {process_id: $process_id})
                    RETURN n, labels(n) as labels
                """, process_id=process_id)
                
                # Get relationships
                edges_result = session.run("""
                    MATCH (a {process_id: $process_id})-[r]->(b {process_id: $process_id})
                    RETURN a, r, b, type(r) as rel_type
                """, process_id=process_id)
                
                # Format for Vis.js
                nodes = []
                edges = []
                
                # Process nodes
                for record in nodes_result:
                    node = record['n']
                    label = record['labels'][0] if record['labels'] else 'Unknown'
                    
                    nodes.append({
                        'id': node.element_id,
                        'label': f"{label}\n{node.get('name', node.get('type', node.get('metal', '')))}",
                        'group': label.lower(),
                        'title': json.dumps(dict(node), indent=2)
                    })
                
                # Process edges
                for record in edges_result:
                    edges.append({
                        'from': record['a'].element_id,
                        'to': record['b'].element_id,
                        'label': record['rel_type'],
                        'arrows': 'to'
                    })
                
                return {
                    'nodes': nodes,
                    'edges': edges,
                    'process_id': process_id
                }
                
        except Exception as e:
            logger.error(f"Failed to get process graph: {e}")
            raise
    
    async def calculate_circularity_metrics(self, process_id: str) -> Dict[str, float]:
        """Calculate circularity metrics using graph algorithms"""
        try:
            with self.driver.session() as session:
                # Calculate recycling loops
                loops_result = session.run("""
                    MATCH path = (n {process_id: $process_id})-[*..10]->(n)
                    WHERE any(rel in relationships(path) WHERE type(rel) IN ['FEEDS_INTO', 'FEEDS_BACK'])
                    RETURN count(path) as loop_count, avg(length(path)) as avg_loop_length
                """, process_id=process_id)
                
                # Calculate material flow efficiency
                efficiency_result = session.run("""
                    MATCH (n {process_id: $process_id})
                    WHERE 'Recycling' in labels(n) OR 'Reprocessing' in labels(n)
                    RETURN avg(n.rate) as avg_recycling_rate, count(n) as recycling_nodes
                """, process_id=process_id)
                
                # Calculate waste streams
                waste_result = session.run("""
                    MATCH (w:Waste {process_id: $process_id})
                    RETURN count(w) as waste_streams
                """, process_id=process_id)
                
                loops = loops_result.single()
                efficiency = efficiency_result.single()
                waste = waste_result.single()
                
                # Calculate composite circularity score
                loop_score = min(100, (loops['loop_count'] or 0) * 10)
                efficiency_score = efficiency['avg_recycling_rate'] or 0
                waste_penalty = (waste['waste_streams'] or 0) * 5
                
                circularity_score = max(0, min(100, 
                    (loop_score * 0.4) + (efficiency_score * 0.5) - waste_penalty
                ))
                
                return {
                    'circularity_score': circularity_score,
                    'loop_count': loops['loop_count'] or 0,
                    'avg_loop_length': loops['avg_loop_length'] or 0,
                    'recycling_efficiency': efficiency_score,
                    'waste_streams': waste['waste_streams'] or 0
                }
                
        except Exception as e:
            logger.error(f"Failed to calculate circularity metrics: {e}")
            return {'circularity_score': 0, 'error': str(e)}
    
    async def find_optimization_paths(self, process_id: str) -> List[Dict[str, Any]]:
        """Find optimization opportunities in the process graph"""
        try:
            with self.driver.session() as session:
                # Find potential short circuits
                shortcuts_result = session.run("""
                    MATCH (start {process_id: $process_id}), (end {process_id: $process_id})
                    WHERE 'Waste' in labels(start) AND 'Processing' in labels(end)
                    MATCH path1 = shortestPath((start)-[*..5]->(end))
                    WHERE length(path1) > 2
                    RETURN start, end, length(path1) as current_length
                """, process_id=process_id)
                
                # Find energy optimization opportunities
                energy_result = session.run("""
                    MATCH (p {process_id: $process_id})
                    WHERE p.energy_source IS NOT NULL
                    AND (p.energy_source CONTAINS 'Coal' OR p.energy_source CONTAINS 'Grid')
                    RETURN p as node, p.energy_consumption as consumption
                """, process_id=process_id)
                
                opportunities = []
                
                # Process shortcuts
                for record in shortcuts_result:
                    opportunities.append({
                        'type': 'circular_loop',
                        'description': f"Connect {record['start'].get('type', 'waste')} directly to {record['end'].get('type', 'processing')}",
                        'impact': 'High',
                        'current_steps': record['current_length'],
                        'optimized_steps': 1
                    })
                
                # Process energy opportunities
                for record in energy_result:
                    node = record['node']
                    opportunities.append({
                        'type': 'energy_optimization',
                        'description': f"Switch {node.get('type', 'process')} to renewable energy",
                        'impact': 'Medium',
                        'current_energy': node.get('energy_source'),
                        'suggested_energy': 'Solar + Wind',
                        'potential_reduction': '25-40% CO2e'
                    })
                
                return opportunities
                
        except Exception as e:
            logger.error(f"Failed to find optimization paths: {e}")
            return []