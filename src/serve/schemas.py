from pydantic import BaseModel

class NEOInput(BaseModel):
    diameter_min_m: float
    diameter_max_m: float
    miss_distance_km: float
    velocity_kph: float

class PredictionOutput(BaseModel):
    is_hazardous: bool