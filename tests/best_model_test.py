import joblib
from sklearn.metrics import classification_report
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/processed/neo_data_balanced.csv")
X = df[["diameter_min_m", "diameter_max_m", "miss_distance_km", "velocity_kph"]]
y = df["is_hazardous"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42, stratify=y
)

model = joblib.load("models/best_model.pkl")
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred, digits=4))