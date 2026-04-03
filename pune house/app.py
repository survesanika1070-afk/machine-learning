# app.py

import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("🏠 House Price Prediction App")

# User inputs
location = st.text_input("Location")
size = st.number_input("Number of BHK", min_value=1)
bath = st.number_input("Number of Bathrooms", min_value=1)
balcony = st.number_input("Number of Balconies", min_value=0)
sqft = st.number_input("Total Square Feet", min_value=100)

if st.button("Predict Price"):
    input_data = {
        "location": location,
        "size": size,
        "bath": bath,
        "balcony": balcony,
        "total_sqft": sqft
    }

    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(df)

    st.success(f"Estimated Price: ₹ {round(prediction[0], 2)}")