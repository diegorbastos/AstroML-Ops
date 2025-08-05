import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os


def load_and_split_data(csv_path: str, test_size: float = 0.4, random_state: int = 42):
    df = pd.read_csv(csv_path)

    #Features e target
    X = df[["diameter_min_m", "diameter_max_m", "miss_distance_km", "velocity_kph"]]
    y = df["is_hazardous"].astype(int)

    #Treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print("Distribuição das classes no conjunto completo:")
    print(df["is_hazardous"].value_counts())

    return X_train, X_test, y_train, y_test

def train_and_evaluate(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)
    print("Modelo Treinado")

    y_pred = model.predict(X_test)

    print("Relatrio de Classificacao")
    print(classification_report(y_test, y_pred, digits=4))

    return model

def save_model(model, output_path="models/random_forest_model.pkl"):
    joblib.dump(model, output_path)
    print(f"Modelo salvo em {output_path}")

if __name__ == "__main__":
    csv_path = "data/processed/neo_data.csv"
    X_train, X_test, y_train, y_test = load_and_split_data(csv_path)

    model = train_and_evaluate(X_train, X_test, y_train, y_test)

    save_model(model)