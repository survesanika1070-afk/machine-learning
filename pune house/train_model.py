# train_model.py

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load dataset
df = pd.read_csv("Pune_House_Data.csv")

# Data cleaning (adjust based on your notebook)
df = df.dropna()

# Example feature selection (modify as per your dataset)
X = df.drop("price", axis=1)
y = df["price"]

# Convert categorical to numeric (if needed)
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("R2 Score:", r2_score(y_test, y_pred))

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save columns (important for prediction)
with open("columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Model trained and saved!")