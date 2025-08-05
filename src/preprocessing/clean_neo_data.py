import os
import json
import pandas as pd

def extract_neo_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    all_objects = []

    for date, objects in data['near_earth_objects'].items():
        for obj in objects:
            try:
                diameter = obj['estimated_diameter']['meters']
                approach = obj['close_approach_data'][0]

                neo_info = {
                    'name': obj['name'],
                    'date': date,
                    'diameter_min_m': diameter['estimated_diameter_min'],
                    'diameter_max_m': diameter['estimated_diameter_max'],
                    'miss_distance_km': float(approach['miss_distance']['kilometers']),
                    'velocity_kph': float(approach['relative_velocity']['kilometers_per_hour']),
                    'is_hazardous': obj['is_potentially_hazardous_asteroid']
                }

                all_objects.append(neo_info)

            except (KeyError, IndexError, TypeError):
                continue

    return pd.DataFrame(all_objects)

if __name__ == "__main__":
    raw_folder = "data/raw"
    output_file = "data/processed/neo_data.csv"

    all_dfs = []
    for file in os.listdir(raw_folder):
        if file.endswith(".json"):
            json_path = os.path.join(raw_folder, file)
            print(f"📄 Processando {json_path}")
            df = extract_neo_data(json_path)
            all_dfs.append(df)

    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)
        full_df = full_df.drop_duplicates().dropna()

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        full_df.to_csv(output_file, index=False)
        print(f"Dados combinados salvos em {output_file} com {len(full_df)} registros.")
    else:
        print("Nenhum arquivo .json encontrado em data/raw/")