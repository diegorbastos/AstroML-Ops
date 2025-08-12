# AstroML Ops — NEO Hazard Classification

I developed **AstroML Ops** as an end-to-end **MLOps pipeline** to process and classify NASA Near-Earth Objects (NEO) data.  
The goal is to identify potentially hazardous asteroids through a fully automated workflow that covers data acquisition, preprocessing, model training, deployment, and continuous monitoring.

This solution integrates **FastAPI** for serving predictions, **MLflow** for experiment tracking and model management, and **Evidently** for data drift detection and reporting.

---

## Project Overview

The pipeline is composed of the following stages:

- **Ingestion** → Automated retrieval of NEO data from NASA’s public API.  
- **Preprocessing** → Feature extraction, data cleaning, and generation of structured datasets.  
- **Training** → RandomForest model (v1.0) with experiment tracking and artifact logging in MLflow.  
- **Serving** → REST API (FastAPI) providing endpoints for predictions, health checks, and model versioning.  
- **Monitoring** → Continuous drift analysis and visual reporting with Evidently.  
- **Pipeline Orchestration** → A single script to execute the entire workflow end-to-end.

---

## Project Structure
```
notebooks/        # Exploratory data analysis and experiments
pipelines/        # Orchestration scripts
src/  
  ingest/         # Data ingestion from NASA API  
  preprocessing/  # Data cleaning and transformation  
  train/          # Model training and MLflow tracking  
  serve/          # FastAPI application and schema definitions  
  evaluate/       # Model drift analysis and reporting  
data/processed/   # Processed datasets  
monitoring/  
  reports/        # Drift and performance reports  
tests/            # API and model validation tests
```

---

## Requirements

- Python **3.11+**  
- (Optional) Docker + Docker Compose  
- NASA API Key → [Request here](https://api.nasa.gov/)

---

## Environment Setup

Create a `.env` file based on `.env.example`:

```
NASA_API_KEY=YOUR_KEY_HERE
```

---

## Running Locally (Without Docker)

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the complete pipeline (ingestion → preprocessing → training → reporting):**
- Windows (PowerShell):
```bash
$env:PYTHONPATH="."; python pipelines/full_pipeline.py
```
- Linux/macOS:
```bash
PYTHONPATH=. python pipelines/full_pipeline.py
```

**Start the API:**
```bash
uvicorn src.serve.main:app --reload
```
API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Running with Docker
```bash
docker compose up --build
```
- API: [http://localhost:8000/docs](http://localhost:8000/docs)  
- MLflow: [http://localhost:5000](http://localhost:5000)  
- Drift reports: `monitoring/reports/*.html`

---

## Monitoring & Experiment Tracking

- **Evidently** → Generates HTML reports comparing:
  - Training data vs current dataset (`drift_report.html`)  
  - Training data vs API inference data (`api_drift_report.html`)
- **MLflow** → Records model parameters, evaluation metrics, confusion matrices, and classification reports.

---

## Skills & Technologies
- **Programming:** Python 3.11+  
- **Machine Learning:** scikit-learn, pandas, NumPy  
- **MLOps & Monitoring:** MLflow, Evidently  
- **API Development:** FastAPI, Uvicorn  
- **Infrastructure:** Docker, Docker Compose  
- **Data Source:** NASA Near-Earth Objects (NEO) API  

---

## Example Prediction

**Request:**
```json
{
  "diameter_min_m": 120.0,
  "diameter_max_m": 250.0,
  "miss_distance_km": 80000,
  "velocity_kph": 90000
}
```

**Response:**
```json
{ "is_hazardous": true }
```