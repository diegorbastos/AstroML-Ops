import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
import os
import mlflow
import mlflow.sklearn


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

def train_and_evaluate(X_train, X_test, y_train, y_test,
                       n_estimators=100, max_depth = None, random_state = 42):
    mlflow.set_experiment("Detecção de NEOs Perigosos")
    with mlflow.start_run():
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            class_weight="balanced"
        )

        model.fit(X_train, y_train)
        #print("Modelo Treinado")

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        print(classification_report(y_test, y_pred, digits=4))

        return model

def save_model(model, output_path="models/random_forest_model.pkl"):
    joblib.dump(model, output_path)
    print(f"Modelo salvo em {output_path}")
    mlflow.log_artifact(output_path)

if __name__ == "__main__":
    csv_path = "data/processed/neo_data_balanced.csv"
    X_train, X_test, y_train, y_test = load_and_split_data(csv_path)

    experimentos = [
        {"n_estimators": 50, "max_depth": 5},
        {"n_estimators": 100, "max_depth": 10},
        {"n_estimators": 200, "max_depth": None},
    ]

    best_model = None
    best_f1 = 0

    for config in experimentos:
        model = train_and_evaluate(
            X_train, X_test, y_train, y_test,
            n_estimators=config["n_estimators"],
            max_depth=config["max_depth"]
        )
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

    save_model(best_model, output_path="models/best_model.pkl")