import os
import sys
from datetime import datetime, timedelta
from glob import glob
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.download_neo_data import download_period
from src.preprocessing.clean_neo_data import extract_neo_data
from src.train.train_model import load_and_split_data, train_and_evaluate, save_model
from src.evaluate.generate_drift_report import gerar_drift_report
from src.evaluate.generate_api_drift_report import gerar_api_drift_report

RAW_DIR = "data/raw"
PROCESSED_FILE = "data/processed/neo_data.csv"
BALANCED_FILE = "data/processed/neo_data_balanced.csv"
MODEL_PATH = "models/best_model.pkl"

def run_pipeline():
    end = datetime.utcnow().date()
    start = end - timedelta(days=30)
    download_period(start, end, RAW_DIR)

    all_dfs = []
    for path in glob(f"{RAW_DIR}/*.json"):
        df = extract_neo_data(path)
        all_dfs.append(df)

    if not all_dfs:
        print("Nenhum dado encontrado.")
        return

    df_full = pd.concat(all_dfs, ignore_index=True)
    df_full = df_full.dropna().drop_duplicates()
    df_full.to_csv(PROCESSED_FILE, index=False)
    print(f"Dados salvos em {PROCESSED_FILE} com {len(df_full)} registros.")

    hazardous = df_full[df_full["is_hazardous"] == True]
    non_hazardous = df_full[df_full["is_hazardous"] == False]
    if not hazardous.empty:
        REPLICATION_FACTOR = 5
        hazardous_upsampled = pd.concat([hazardous] * REPLICATION_FACTOR, ignore_index=True)
        df_balanced = pd.concat([hazardous_upsampled, non_hazardous], ignore_index=True)
        df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)
        df_balanced.to_csv(BALANCED_FILE, index=False)
        print(f"Dados balanceados salvos em {BALANCED_FILE}")
    else:
        print("Nenhum NEO perigoso encontrado para balancear.")

    X_train, X_test, y_train, y_test = load_and_split_data(BALANCED_FILE)
    model = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_model(model, output_path=MODEL_PATH)

    gerar_drift_report()
    gerar_api_drift_report()

    print("Pipeline completa executada com sucesso!")

if __name__ == "__main__":
    run_pipeline()