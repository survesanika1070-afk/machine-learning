import pickle

# Load model
with open("student_model.pkl", "rb") as f:
    model = pickle.load(f)

# Input (example)
hours = float(input("Enter study hours: "))

# Prediction
prediction = model.predict([[hours]])

print(f"Predicted Score: {prediction[0]}")