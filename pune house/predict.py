# predict.py

import pickle
import numpy as np
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

def predict_price(input_data):
    """
    input_data: dictionary of features
    """
    df = pd.DataFrame([input_data])
    
    # Ensure same columns
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)
    
    prediction = model.predict(df)
    return prediction[0]


# Example usage
if __name__ == "__main__":
    sample = {
        "location": "Baner",
        "size": 2,
        "bath": 2,
        "balcony": 1,
        "total_sqft": 1000
    }

    price = predict_price(sample)
    print("Predicted Price:", price)