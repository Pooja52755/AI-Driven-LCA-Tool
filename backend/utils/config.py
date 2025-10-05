from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Settings
    api_title: str = "AI-Driven LCA Tool for Metallurgy"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Database Settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "gubRIbo598w3uRcT74bvJNfzO9--USWUM7Bd45BgauE"
    database_url: str = "sqlite:///./lca_data.db"
    
    # ML Model Settings
    model_path: str = "./ml-models"
    lightgbm_model_path: str = "./ml-models/lightgbm_lca_model.pkl"
    circularity_model_path: str = "./ml-models/circularity_model.pkl"
    
    # Data Settings
    mock_data_path: str = "./data/mock_metallurgy_data.json"
    
    # spaCy Settings
    spacy_model: str = "en_core_web_sm"
    
    # Performance Settings
    max_workers: int = 4
    prediction_timeout: int = 30  # seconds
    graph_query_timeout: int = 60  # seconds
    
    # Security Settings
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    # JNARDDC Specific Settings
    jnarddc_data_source: str = "https://jnarddc.gov.in/data"
    bis_compliance: bool = True
    indian_energy_factors: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()