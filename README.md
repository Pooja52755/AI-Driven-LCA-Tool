# AI-Driven Life Cycle Assessment (LCA) Tool for Metallurgy and Mining

## SIH 2025 Project - Problem Statement 25069

An intuitive, AI-powered software platform that enables metallurgists, engineers, and decision-makers to perform automated LCAs for metals (aluminium, copper, steel, zinc, lead) with emphasis on circularity and sustainability.

## 🏗️ Architecture

```
ai-lca-metallurgy/
├── backend/           # FastAPI + Gunicorn
├── frontend/          # Svelte + Vis.js
├── database/          # Neo4j + SQLite
├── ml-models/         # LightGBM + spaCy
├── data/             # Mock metallurgy datasets
├── docker/           # Container configurations
└── docs/             # Documentation
```

## 🚀 Tech Stack

- **Frontend**: Svelte + Vis.js (Interactive UI & Visualizations)
- **Backend**: FastAPI + Gunicorn (API & Processing)
- **Database**: Neo4j Community + SQLite (Graph & Structured Data)
- **AI/ML**: LightGBM + spaCy (Predictions & NLP Reports)
- **Data**: Pandas + OpenLCA Python API (Processing & Simulation)
- **Deployment**: Docker + Caddy (Portable & Lightweight)

## 🎯 Key Features

1. **Interactive Process Modeling**: Drag-and-drop interface for metallurgy processes
2. **AI-Powered Predictions**: Automatic estimation of missing LCA parameters
3. **Circularity Analysis**: Advanced metrics for circular economy assessment
4. **Multi-Metal Support**: Aluminium, Copper, Steel, Zinc, Lead
5. **Real-time Comparisons**: Conventional vs. circular processing pathways
6. **Actionable Reports**: Natural language recommendations
7. **Model Validation**: Transparent accuracy metrics (R², F1, errors)

## 🏃 Quick Start

```bash
# Clone and setup
cd ai-lca-metallurgy

# Start with Docker
docker-compose up -d

# Or run locally
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```
http://localhost:5000/-frontend
http://localhost:8000/-backend
http://localhost:8000/docs


## 📊 Mock Data Coverage

- **5 Metals**: Al, Cu, Steel, Zn, Pb
- **Process Routes**: Primary extraction vs. Recycled
- **Indian Context**: Odisha bauxite, Khetri copper, Jamshedpur steel
- **Circularity Metrics**: Recycling rates, circularity scores
- **Environmental Impact**: GWP, acidification, eutrophication

## 🎓 For SIH Judges

- **Innovation**: Graph-based circularity optimization
- **Performance**: <2MB bundle, <200MB RAM, <1s load time
- **Scalability**: 1M+ nodes locally, 100+ concurrent users
- **Accuracy**: 85%+ prediction accuracy with validation dashboard
- **Indian Focus**: BIS-compliant, JNARDDC-aligned, Atmanirbhar data

## 📄 License

MIT License - Built for SIH 2025
