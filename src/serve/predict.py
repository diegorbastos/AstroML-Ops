import pandas as pd

def predict_hazard(model, input_data: dict) -> bool:
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    return bool(prediction[0])