import streamlit as st
import pickle

# Load model
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

# Title
st.title("🌸 Iris Flower Prediction App")

st.write("Enter flower measurements to predict species")

# Inputs
sepal_length = st.slider("Sepal Length", 4.0, 8.0, 5.0)
sepal_width = st.slider("Sepal Width", 2.0, 4.5, 3.0)
petal_length = st.slider("Petal Length", 1.0, 7.0, 4.0)
petal_width = st.slider("Petal Width", 0.1, 2.5, 1.0)

# Prediction
if st.button("Predict"):
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

    labels = ["Setosa", "Versicolor", "Virginica"]

    st.success(f"🌼 Predicted Flower: {labels[prediction[0]]}")