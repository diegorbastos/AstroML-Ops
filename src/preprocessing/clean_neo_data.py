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
                continue  # pula objetos com dados faltando

    return pd.DataFrame(all_objects)

if __name__ == "__main__":
    input_file = "data/raw/neo_2025-07-30_2025-08-01.json"
    output_file = "data/processed/neo_data.csv"

    df = extract_neo_data(input_file)

    df.to_csv(output_file, index=False)
    print(f"CSV salvo em {output_file} com {len(df)} registros.")