import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# Dataset
data = {
    "Hours": [1,2,3,4,5,6,7,8,9,10],
    "Scores": [10,20,30,40,50,60,70,80,90,100]
}

df = pd.DataFrame(data)

# Features & Labels
X = df[["Hours"]]
y = df["Scores"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
with open("student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")