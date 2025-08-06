import joblib
import os

def load_model(model_path: str = "models/best_model.pkl"):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
    return joblib.load(model_path)