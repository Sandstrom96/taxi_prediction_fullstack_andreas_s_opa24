from importlib.resources import files

TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
CLEAN_TAXI_CSV_PATH = files("taxipred").joinpath("data/cleaned_taxi_trip_pricing.csv")
MODELS_PATH = files("taxipred").joinpath("models")

# DATA_PATH = Path(__file__).parents[1] / "data"
