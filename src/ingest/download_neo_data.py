import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv.main import load_dotenv

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
API_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def download_period(start_date, end_date, output_folder="data/raw"):
    os.makedirs(output_folder, exist_ok=True)
    current = start_date

    while current <= end_date:
        period_end = min(current + timedelta(days=6), end_date)
        filename = f"neo_{current}_{period_end}.json"
        output_path = os.path.join(output_folder, filename)

        if not os.path.exists(output_path):  # evita sobrescrever
            params = {
                "start_date": current.strftime("%Y-%m-%d"),
                "end_date": period_end.strftime("%Y-%m-%d"),
                "api_key": NASA_API_KEY
            }

            print(f"Baixando {params['start_date']} até {params['end_date']}...")
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                with open(output_path, "w") as f:
                    json.dump(response.json(), f, indent=2)
                print(f"Salvo em {output_path}")
            else:
                print(f"Erro {response.status_code}: {response.text}")
        else:
            print(f"Já existe: {output_path}")

        current = period_end + timedelta(days=1)


if __name__ == "__main__":
    end = datetime.utcnow().date()
    start = end - timedelta(days=30)
    download_period(start, end)