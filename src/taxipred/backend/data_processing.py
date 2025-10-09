from taxipred.utils.constants import CLEAN_TAXI_CSV_PATH
import pandas as pd
import json
from pydantic import BaseModel, Field


class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(CLEAN_TAXI_CSV_PATH)

    def to_json(self):
        return json.loads(self.df.to_json(orient="records"))


class TripInput(BaseModel):
    Trip_Distance_km: float = Field(25.3, gt=1.0)
    Time_of_Day: str = Field("Morning", pattern="^(Morning|Afternoon|Evening|Night)$")
    Day_of_Week: str = Field("Weekday", pattern="^(Weekday|Weekend)$")


class PredictionOutput(BaseModel):
    predicted_trip_price: float
