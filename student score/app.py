import streamlit as st
import pickle

# Load model
with open("student_model.pkl", "rb") as f:
    model = pickle.load(f)

# Title
st.title("🎓 Student Score Predictor")

st.write("Enter number of hours studied to predict score")

# Input
hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, step=0.5)

# Button
if st.button("Predict"):
    prediction = model.predict([[hours]])
    st.success(f"📊 Predicted Score: {prediction[0]:.2f}")