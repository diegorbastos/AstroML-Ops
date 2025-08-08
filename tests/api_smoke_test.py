import requests

BASE = "http://localhost:8000"

def ping_health():
    r = requests.get(f"{BASE}/health", timeout=5)
    print("Health:", r.status_code, r.json())

def predict(payload):
    r = requests.post(f"{BASE}/predict", json=payload, timeout=10)
    print("Input:", payload)
    print("Output:", r.status_code, r.json())
    print("-" * 40)

if __name__ == "__main__":
    ping_health()

    predict({
        "diameter_min_m": 10,
        "diameter_max_m": 30,
        "miss_distance_km": 5000000,
        "velocity_kph": 40000
    })

    predict({
        "diameter_min_m": 120,
        "diameter_max_m": 250,
        "miss_distance_km": 80000,
        "velocity_kph": 90000
    })
