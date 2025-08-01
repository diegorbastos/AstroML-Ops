import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
API_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def download_neo_data(start_date: str, end_date: str, output_path: str):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY
    }

    print(f"Buscando dados de {start_date} até {end_date}...")
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Dados salvos em: {output_path}")
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    end = datetime.utcnow().date()
    start = end - timedelta(days=2)
    filename = f"neo_{start}_{end}.json"
    output_file = f"data/raw/{filename}"

    download_neo_data(str(start), str(end), output_file)