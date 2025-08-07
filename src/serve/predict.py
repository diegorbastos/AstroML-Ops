import pandas as pd
import csv
import os
from datetime import datetime

def log_inference(input_data: dict, prediction: bool, log_path="monitoring/logs/inferences.csv"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.isfile(log_path)

    with open(log_path, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "timestamp", "diameter_min_m", "diameter_max_m",
            "miss_distance_km", "velocity_kph", "is_hazardous"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "diameter_min_m": input_data["diameter_min_m"],
            "diameter_max_m": input_data["diameter_max_m"],
            "miss_distance_km": input_data["miss_distance_km"],
            "velocity_kph": input_data["velocity_kph"],
            "is_hazardous": prediction
        })

def predict_hazard(model, input_data: dict) -> bool:
    df = pd.DataFrame([input_data])
    prediction = bool(model.predict(df)[0])

    log_inference(input_data, prediction)

    return prediction