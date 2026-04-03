import pickle
import numpy as np
from pathlib import Path

MODEL_PATH = Path(r"C:\Users\inter\Desktop\sanika surve\Machine learning\pune house\model.pkl")
COLUMNS_PATH = Path(r"C:\Users\inter\Desktop\sanika surve\Machine learning\pune house\columns.pkl")


def load_model(path=MODEL_PATH):
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model


def load_columns(path=COLUMNS_PATH):
    with open(path, "rb") as f:
        columns = pickle.load(f)
    if isinstance(columns, dict) and "data_columns" in columns:
        return columns["data_columns"]
    if isinstance(columns, list):
        return columns
    raise ValueError("columns.pkl must contain either a list of columns or a dict with 'data_columns'")


def make_feature_vector(location, bhk, bath, balcony, sqft, area_type, availability, data_columns):
    x = np.zeros(len(data_columns), dtype=float)
    x[0] = bath
    x[1] = balcony
    x[2] = bhk
    x[3] = sqft

    def set_dummy(col_label):
        if col_label in data_columns:
            idx = data_columns.index(col_label)
            x[idx] = 1

    if location and location != "other":
        set_dummy(location)
    if area_type and area_type != "Super built-up  Area":
        set_dummy(area_type)
    if availability and availability != "Not Ready":
        set_dummy(availability)

    return x


def predict_house_price(location, bhk, bath, balcony, sqft, area_type, availability, model=None, data_columns=None):
    if model is None:
        model = load_model()
    if data_columns is None:
        data_columns = load_columns()

    x = make_feature_vector(location, bhk, bath, balcony, sqft, area_type, availability, data_columns)
    y_pred = model.predict([x])
    return y_pred[0]


def predict_house_price_from_dict(raw_data, model=None, data_columns=None):
    required = ["location", "bhk", "bath", "balcony", "sqft", "area_type", "availability"]
    if not all(k in raw_data for k in required):
        missing = [k for k in required if k not in raw_data]
        raise ValueError(f"Missing required keys: {missing}")

    return predict_house_price(
        location=raw_data["location"],
        bhk=raw_data["bhk"],
        bath=raw_data["bath"],
        balcony=raw_data["balcony"],
        sqft=raw_data["sqft"],
        area_type=raw_data["area_type"],
        availability=raw_data["availability"],
        model=model,
        data_columns=data_columns,
    )


if __name__ == "__main__":
    sample = {
        "location": "Hadapsar",
        "bhk": 2,
        "bath": 2,
        "balcony": 2,
        "sqft": 1000,
        "area_type": "Super built-up  Area",
        "availability": "Ready To Move",
    }
    model = load_model()
    price = predict_house_price_from_dict(sample, model=model)
    print("Predicted price:", price)

