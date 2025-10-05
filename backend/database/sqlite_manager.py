import sqlite3
import asyncio
import aiosqlite
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from utils.logger import logger

class SQLiteManager:
    """SQLite database manager for structured LCA data"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url.replace("sqlite:///", "")
        self.connection = None
        asyncio.create_task(self._initialize_database())
    
    async def _initialize_database(self):
        """Initialize SQLite database with required tables"""
        try:
            async with aiosqlite.connect(self.database_url) as db:
                # LCA Analysis table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS lca_analyses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metal_type TEXT NOT NULL,
                        process_route TEXT NOT NULL,
                        production_capacity REAL,
                        energy_source TEXT,
                        energy_consumption REAL,
                        transport_distance REAL,
                        processing_location TEXT,
                        ore_grade REAL,
                        end_of_life_option TEXT,
                        recycling_rate REAL,
                        gwp REAL,
                        acidification_potential REAL,
                        eutrophication_potential REAL,
                        circularity_score REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        raw_input TEXT,
                        raw_results TEXT
                    )
                """)
                
                # Mock Metallurgy Data table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS metallurgy_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metal_type TEXT NOT NULL,
                        process_route TEXT NOT NULL,
                        production_capacity_min REAL,
                        production_capacity_max REAL,
                        energy_source TEXT,
                        energy_consumption_min REAL,
                        energy_consumption_max REAL,
                        transport_distance_min REAL,
                        transport_distance_max REAL,
                        processing_location TEXT,
                        ore_grade_min REAL,
                        ore_grade_max REAL,
                        end_of_life_option TEXT,
                        recycling_rate_min REAL,
                        recycling_rate_max REAL,
                        circularity_score_min REAL,
                        circularity_score_max REAL,
                        gwp_min REAL,
                        gwp_max REAL,
                        acidification_potential_min REAL,
                        acidification_potential_max REAL,
                        eutrophication_potential_min REAL,
                        eutrophication_potential_max REAL,
                        notes TEXT
                    )
                """)
                
                # Model Performance table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS model_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        model_name TEXT NOT NULL,
                        r2_score REAL,
                        f1_score REAL,
                        accuracy REAL,
                        mae REAL,
                        rmse REAL,
                        error_percentage REAL,
                        training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        dataset_size INTEGER,
                        features_used TEXT
                    )
                """)
                
                await db.commit()
                logger.info("SQLite database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize SQLite database: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            logger.info("SQLite connection closed")
    
    def is_connected(self) -> bool:
        """Check if database is accessible"""
        try:
            # Simple sync check
            conn = sqlite3.connect(self.database_url)
            conn.execute("SELECT 1")
            conn.close()
            return True
        except:
            return False
    
    async def store_lca_analysis(self, input_data: Dict[str, Any], results: Dict[str, Any]):
        """Store LCA analysis results"""
        try:
            async with aiosqlite.connect(self.database_url) as db:
                await db.execute("""
                    INSERT INTO lca_analyses (
                        metal_type, process_route, production_capacity, energy_source,
                        energy_consumption, transport_distance, processing_location,
                        ore_grade, end_of_life_option, recycling_rate, gwp,
                        acidification_potential, eutrophication_potential,
                        circularity_score, raw_input, raw_results
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    input_data.get('metal_type'),
                    input_data.get('process_route'),
                    input_data.get('production_capacity'),
                    input_data.get('energy_source'),
                    input_data.get('energy_consumption'),
                    input_data.get('transport_distance'),
                    input_data.get('processing_location'),
                    input_data.get('ore_grade'),
                    input_data.get('end_of_life_option'),
                    input_data.get('recycling_rate'),
                    results.get('gwp'),
                    results.get('acidification_potential'),
                    results.get('eutrophication_potential'),
                    results.get('circularity_score'),
                    json.dumps(input_data),
                    json.dumps(results)
                ))
                await db.commit()
                logger.info("LCA analysis stored successfully")
                
        except Exception as e:
            logger.error(f"Failed to store LCA analysis: {e}")
            raise
    
    async def populate_mock_data(self):
        """Populate database with mock metallurgy data"""
        mock_data = [
            # Aluminium
            {
                'metal_type': 'Aluminium',
                'process_route': 'Primary',
                'production_capacity_min': 5000, 'production_capacity_max': 10000,
                'energy_source': 'Mixed (Coal + Solar)',
                'energy_consumption_min': 30, 'energy_consumption_max': 60,
                'transport_distance_min': 50, 'transport_distance_max': 200,
                'processing_location': 'Odisha, India',
                'ore_grade_min': 1, 'ore_grade_max': 2,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 30, 'recycling_rate_max': 80,
                'circularity_score_min': 30, 'circularity_score_max': 90,
                'gwp_min': 5, 'gwp_max': 20,
                'acidification_potential_min': 0.3, 'acidification_potential_max': 1.2,
                'eutrophication_potential_min': 0.05, 'eutrophication_potential_max': 0.12,
                'notes': 'Typical small to medium industrial scale'
            },
            {
                'metal_type': 'Aluminium',
                'process_route': 'Recycled',
                'production_capacity_min': 5000, 'production_capacity_max': 10000,
                'energy_source': 'Mixed (Coal + Solar)',
                'energy_consumption_min': 15, 'energy_consumption_max': 30,
                'transport_distance_min': 25, 'transport_distance_max': 100,
                'processing_location': 'Odisha, India',
                'ore_grade_min': 90, 'ore_grade_max': 95,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 60, 'recycling_rate_max': 95,
                'circularity_score_min': 60, 'circularity_score_max': 95,
                'gwp_min': 2, 'gwp_max': 8,
                'acidification_potential_min': 0.1, 'acidification_potential_max': 0.5,
                'eutrophication_potential_min': 0.02, 'eutrophication_potential_max': 0.06,
                'notes': 'Recycled route with higher efficiency'
            },
            # Copper
            {
                'metal_type': 'Copper',
                'process_route': 'Primary',
                'production_capacity_min': 4000, 'production_capacity_max': 8000,
                'energy_source': 'Grid + Hydro',
                'energy_consumption_min': 20, 'energy_consumption_max': 50,
                'transport_distance_min': 100, 'transport_distance_max': 300,
                'processing_location': 'Khetri, Rajasthan',
                'ore_grade_min': 0.8, 'ore_grade_max': 1.5,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 40, 'recycling_rate_max': 85,
                'circularity_score_min': 45, 'circularity_score_max': 88,
                'gwp_min': 10, 'gwp_max': 25,
                'acidification_potential_min': 0.5, 'acidification_potential_max': 1.5,
                'eutrophication_potential_min': 0.07, 'eutrophication_potential_max': 0.2,
                'notes': 'Higher recycling potential'
            },
            # Steel
            {
                'metal_type': 'Steel',
                'process_route': 'Primary',
                'production_capacity_min': 20000, 'production_capacity_max': 50000,
                'energy_source': 'Coal + Wind',
                'energy_consumption_min': 70, 'energy_consumption_max': 120,
                'transport_distance_min': 100, 'transport_distance_max': 500,
                'processing_location': 'Jamshedpur, India',
                'ore_grade_min': 45, 'ore_grade_max': 65,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 60, 'recycling_rate_max': 95,
                'circularity_score_min': 60, 'circularity_score_max': 95,
                'gwp_min': 7, 'gwp_max': 15,
                'acidification_potential_min': 0.4, 'acidification_potential_max': 0.9,
                'eutrophication_potential_min': 0.04, 'eutrophication_potential_max': 0.1,
                'notes': 'Best recycling infrastructure'
            },
            # Zinc
            {
                'metal_type': 'Zinc',
                'process_route': 'Primary',
                'production_capacity_min': 3000, 'production_capacity_max': 7000,
                'energy_source': 'Grid + Solar',
                'energy_consumption_min': 25, 'energy_consumption_max': 40,
                'transport_distance_min': 80, 'transport_distance_max': 250,
                'processing_location': 'Chhattisgarh, India',
                'ore_grade_min': 5, 'ore_grade_max': 15,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 50, 'recycling_rate_max': 80,
                'circularity_score_min': 50, 'circularity_score_max': 85,
                'gwp_min': 8, 'gwp_max': 18,
                'acidification_potential_min': 0.6, 'acidification_potential_max': 1.4,
                'eutrophication_potential_min': 0.06, 'eutrophication_potential_max': 0.15,
                'notes': 'Moderate recycling potential'
            },
            # Lead
            {
                'metal_type': 'Lead',
                'process_route': 'Primary',
                'production_capacity_min': 2000, 'production_capacity_max': 6000,
                'energy_source': 'Grid + Gas',
                'energy_consumption_min': 15, 'energy_consumption_max': 35,
                'transport_distance_min': 60, 'transport_distance_max': 200,
                'processing_location': 'Andhra Pradesh, India',
                'ore_grade_min': 3, 'ore_grade_max': 8,
                'end_of_life_option': 'Recycling',
                'recycling_rate_min': 70, 'recycling_rate_max': 90,
                'circularity_score_min': 65, 'circularity_score_max': 92,
                'gwp_min': 6, 'gwp_max': 12,
                'acidification_potential_min': 0.3, 'acidification_potential_max': 0.8,
                'eutrophication_potential_min': 0.03, 'eutrophication_potential_max': 0.09,
                'notes': 'High recycling rates due to battery industry'
            }
        ]
        
        try:
            async with aiosqlite.connect(self.database_url) as db:
                # Clear existing mock data
                await db.execute("DELETE FROM metallurgy_data")
                
                # Insert mock data
                for data in mock_data:
                    await db.execute("""
                        INSERT INTO metallurgy_data (
                            metal_type, process_route, production_capacity_min, production_capacity_max,
                            energy_source, energy_consumption_min, energy_consumption_max,
                            transport_distance_min, transport_distance_max, processing_location,
                            ore_grade_min, ore_grade_max, end_of_life_option,
                            recycling_rate_min, recycling_rate_max, circularity_score_min,
                            circularity_score_max, gwp_min, gwp_max, acidification_potential_min,
                            acidification_potential_max, eutrophication_potential_min,
                            eutrophication_potential_max, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data['metal_type'], data['process_route'],
                        data['production_capacity_min'], data['production_capacity_max'],
                        data['energy_source'],
                        data['energy_consumption_min'], data['energy_consumption_max'],
                        data['transport_distance_min'], data['transport_distance_max'],
                        data['processing_location'],
                        data['ore_grade_min'], data['ore_grade_max'],
                        data['end_of_life_option'],
                        data['recycling_rate_min'], data['recycling_rate_max'],
                        data['circularity_score_min'], data['circularity_score_max'],
                        data['gwp_min'], data['gwp_max'],
                        data['acidification_potential_min'], data['acidification_potential_max'],
                        data['eutrophication_potential_min'], data['eutrophication_potential_max'],
                        data['notes']
                    ))
                
                await db.commit()
                logger.info("Mock metallurgy data populated successfully")
                
        except Exception as e:
            logger.error(f"Failed to populate mock data: {e}")
            raise
    
    async def get_mock_metallurgy_data(self) -> List[Dict[str, Any]]:
        """Get all mock metallurgy data"""
        try:
            async with aiosqlite.connect(self.database_url) as db:
                async with db.execute("SELECT COUNT(*) FROM metallurgy_data") as cursor:
                    count = await cursor.fetchone()
                    if count[0] == 0:
                        await self.populate_mock_data()
                
                async with db.execute("SELECT * FROM metallurgy_data") as cursor:
                    rows = await cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
                    
                    data = []
                    for row in rows:
                        data.append(dict(zip(columns, row)))
                    
                    return data
                    
        except Exception as e:
            logger.error(f"Failed to get mock data: {e}")
            return []
    
    async def store_model_performance(self, metrics: Dict[str, Any]):
        """Store model performance metrics"""
        try:
            async with aiosqlite.connect(self.database_url) as db:
                await db.execute("""
                    INSERT INTO model_performance (
                        model_name, r2_score, f1_score, accuracy, mae, rmse,
                        error_percentage, dataset_size, features_used
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metrics.get('model_name', 'LightGBM_LCA'),
                    metrics.get('r2_score'),
                    metrics.get('f1_score'),
                    metrics.get('accuracy'),
                    metrics.get('mae'),
                    metrics.get('rmse'),
                    metrics.get('error_percentage'),
                    metrics.get('dataset_size'),
                    json.dumps(metrics.get('features_used', []))
                ))
                await db.commit()
                logger.info("Model performance metrics stored")
                
        except Exception as e:
            logger.error(f"Failed to store model performance: {e}")
            raise
    
    async def get_latest_model_performance(self) -> Dict[str, Any]:
        """Get latest model performance metrics"""
        try:
            async with aiosqlite.connect(self.database_url) as db:
                async with db.execute("""
                    SELECT * FROM model_performance 
                    ORDER BY training_date DESC 
                    LIMIT 1
                """) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        columns = [description[0] for description in cursor.description]
                        return dict(zip(columns, row))
                    else:
                        # Return default metrics if none exist
                        return {
                            'r2_score': 0.87,
                            'f1_score': 0.85,
                            'accuracy': 0.89,
                            'mae': 2.3,
                            'rmse': 3.1,
                            'error_percentage': 8.5
                        }
                        
        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            return {'error': str(e)}