from fastapi import FastAPI
from src.serve.model_loader import load_model
from src.serve.predict import predict_hazard
from src.serve.schemas import NEOInput, PredictionOutput

app = FastAPI()
model = load_model()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():
    return {"model_version": "1.0"}

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: NEOInput):
    result = predict_hazard(model, input_data.dict())
    return PredictionOutput(is_hazardous=result)