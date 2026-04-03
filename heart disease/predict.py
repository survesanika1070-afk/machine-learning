import pickle
import numpy as np

# Load model & scaler
model = pickle.load(open("heart_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Input values
print("Enter patient details:")

age = float(input("Age: "))
sex = float(input("Sex (1=Male, 0=Female): "))
cp = float(input("Chest Pain Type (0-3): "))
trestbps = float(input("Resting BP: "))
chol = float(input("Cholesterol: "))
fbs = float(input("Fasting Blood Sugar (1/0): "))
restecg = float(input("Rest ECG (0-2): "))
thalach = float(input("Max Heart Rate: "))
exang = float(input("Exercise Angina (1/0): "))
oldpeak = float(input("Oldpeak: "))
slope = float(input("Slope (0-2): "))

# Create input array
data = np.array([[age, sex, cp, trestbps, chol, fbs,
                  restecg, thalach, exang, oldpeak,
                  slope]])

# Scale
data = scaler.transform(data)

# Predict
prediction = model.predict(data)

if prediction[0] == 1:
    print("⚠️ Heart Disease Detected")
else:
    print("✅ No Heart Disease")