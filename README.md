# LAND SLIDE RISK MONITORING SYSTEM

A full-stack landslide risk monitoring and prediction system designed to analyze rainfall, terrain, flood risk, and environmental factors to identify high-risk areas. The system includes a dashboard, risk visualization, API backend, predictive models, and an interactive frontend.

## Overview

This project helps in:
- Monitoring landslide-prone regions
- Predicting risk levels using machine learning
- Visualizing rainfall and risk patterns
- Showing high-risk areas on an interactive dashboard
- Supporting early warning and decision-making

## Features

- Landslide risk prediction using trained ML models
- Dashboard with charts and risk summaries
- Flood and rainfall-based risk analysis
- High-risk area identification
- REST API backend for prediction services
- Frontend web interface for visual monitoring
- Data preprocessing and model evaluation pipeline

## Tech Stack

- Python
- FastAPI
- React
- Tailwind CSS
- Pandas, NumPy
- scikit-learn
- XGBoost
- LightGBM
- CatBoost
- Matplotlib / Seaborn

## Project Structure

text
LAND SLIDE RISK MONITORING SYSTEM (1)/
├── README.md
├── start_backend.bat
├── start_frontend.bat
├── start_system.bat
├── .gitignore
├── EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── model_loader.py
│   │   ├── predictor.py
│   │   ├── requirements.txt
│   │   └── schemas.py
│   ├── frontend/
│   │   ├── package.json
│   │   ├── postcss.config.js
│   │   ├── tailwind.config.js
│   │   └── src/
│   ├── scripts/
│   │   ├── export_model.py
│   │   └── verify_model.py
│   ├── Global_Landslide_Catalog_Export.csv
│   ├── district wise rainfall normal.csv
│   ├── landslide_dataset.csv
│   ├── urban_pluvial_flood_risk_dataset.csv
│   ├── Untitled0 (1).ipynb
│   └── ...
└── ...

##Activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

##Install backend dependencies
cd "EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER"
pip install -r backend/requirements.txt

##Install frontend dependencies
cd frontend
npm install

###Run the Application
Backend
cd "EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER"
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

Frontend
cd "EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER/frontend"
npm run dev


