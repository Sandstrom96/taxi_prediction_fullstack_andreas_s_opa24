from fastapi import FastAPI
from taxipred.backend.data_processing import TaxiData, TripInput, PredictionOutput
import pandas as pd
import joblib
from taxipred.utils.constants import MODELS_PATH

app = FastAPI()

taxi_data = TaxiData()


@app.get("/taxi/")
async def read_taxi_data():
    return taxi_data.to_json()


@app.post("/taxi/predict", response_model=PredictionOutput)
def predict_trip_price(payload: TripInput):
    preditction_data = pd.DataFrame([payload])

    # Load the trained model, the used scaler and encoded_columns from training
    model = joblib.load(MODELS_PATH / "model.joblib")
    scaler = joblib.load(MODELS_PATH / "scaler.joblib")
    encoded_columns = joblib.load(MODELS_PATH / "encoded_columns.joblib")

    # Encoding the categorical features
    encoded_data = pd.get_dummies(
        preditction_data, columns=["Time_of_Day", "Day_of_Week"]
    )
    # Reindexing to ensure the columns match the trained data
    encoded_data = encoded_data.reindex(columns=encoded_columns, fill_value=0)
    # If hte model used a scaler, scale the data
    if scaler is not None:
        encoded_data = scaler.transform(encoded_data)

    preditction = model.predict(encoded_data)
    return {"predicted_trip_price": preditction[0]}


if __name__ == "__main__":
    new_trips = {
        "Base_Fare": 3.5,
        "Trip_Distance_km": 19,
        "Time_of_Day": "Morning",
        "Day_of_Week": "Weekday",
    }

    print(predict_trip_price(new_trips))
