# 🚀 AstroML Ops — NEO Hazard Classification (v1.0.0)

A complete **MLOps pipeline** to download NASA NEO (Near-Earth Objects) data, preprocess it, train a classifier for potentially hazardous asteroids, serve predictions via a FastAPI API, and monitor model drift with **Evidently** and experiment tracking with **MLflow**.

---

## 🔭 Overview
- **Ingestion** → Fetches NEO data from NASA's public API.
- **Preprocessing** → Extracts relevant features, cleans data, and stores CSVs.
- **Training** → RandomForest model (v1.0) with experiment logging in MLflow.
- **Serving** → FastAPI REST API with `/predict`, `/health`, `/version` endpoints.
- **Monitoring** → Drift detection with Evidently (HTML reports).
- **Pipeline** → Single script to orchestrate the entire flow.

---

## 🧱 Project Structure

├── notebooks/ # Jupyter notebook for EDA and experiments
├── pipelines/ # Full pipeline orchestration  
├── src/  
│ ├── ingest/ # Data download from NASA  
│ ├── preprocessing/ # Data cleaning and processing  
│ ├── train/ # Model training + MLflow tracking  
│ ├── serve/ # FastAPI app, prediction, schema  
│ └── evaluate/ # Drift reports with Evidently  
├── data/processed/ # Processed CSVs  
├── monitoring/  
│ ├── reports/ # Drift reports, confusion matrix  
├── tests/ # Smoke tests for API and best model test
├── requirements.txt  
├── docker-compose.yml  
├── Dockerfile  
├── .env.example  
└── README.md

---

## ⚙️ Requirements
- Python **3.11+**
- (Optional) Docker + Docker Compose
- NASA API key → [Get here](https://api.nasa.gov/)

---

## 🔑 Environment Variables
Create a `.env` file based on `.env.example`:  
`NASA_API_KEY=YOUR_KEY_HERE`

---

## 🚀 Running Locally (without Docker)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run full pipeline (ingest → preprocess → train → drift reports)

**Windows (PowerShell):**
```bash
$env:PYTHONPATH="."; python pipelines/full_pipeline.py
```

**Linux/macOS:**
```bash
PYTHONPATH=. python pipelines/full_pipeline.py
```

### Start API
```bash
uvicorn src.serve.main:app --reload
```
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Running with Docker
```bash
docker compose up --build
```
- API → [http://localhost:8000/docs](http://localhost:8000/docs)
- MLflow → [http://localhost:5000](http://localhost:5000)
- Drift reports → `monitoring/reports/*.html`

---

## 🔍 Monitoring & Tracking
- **Evidently** → HTML reports for:
  - Training vs Current Data (drift_report.html)
  - Training vs API Inferences (api_drift_report.html)

- **MLflow** → parameters, metrics, confusion matrix, classification report.

---

## 🧪 API Endpoints
- **GET /health** → Health check
- **GET /version** → Model version
- **POST /predict** → Example request:

```json
{
  "diameter_min_m": 120.0,
  "diameter_max_m": 250.0,
  "miss_distance_km": 80000,
  "velocity_kph": 90000
}
```

Response:
```json
{ "is_hazardous": true }
```

---

## ⚠ Known Issues
- **Inflated F1-score** → Current version uses oversampling on the entire dataset, which may lead to unrealistically high F1.
- **Unrealistic inputs** → Very atypical or extreme values may result in unexpected predictions.

---

## 🗺 Future Versions
- Oversample only on training set
- Cross-validation and hyperparameter tuning