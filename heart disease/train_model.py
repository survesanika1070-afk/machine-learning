import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Load dataset (make sure heart.csv is in same folder)
df = pd.read_csv("heart.csv")

# Features & target
if "target" in df.columns:
    target_col = "target"
elif "HeartDisease" in df.columns:
    target_col = "HeartDisease"
else:
    raise ValueError("Target column not found. Expected 'target' or 'HeartDisease'.")

# Convert categorical text labels to numeric codes matching model input expectations
encoding_maps = {
    "Sex": {"M": 1, "F": 0},
    "ChestPainType": {"TA": 0, "ATA": 1, "NAP": 2, "ASY": 3},
    "RestingECG": {"Normal": 0, "ST": 1, "LVH": 2},
    "ExerciseAngina": {"N": 0, "Y": 1},
    "ST_Slope": {"Up": 2, "Flat": 1, "Down": 0},
}

for col, mapping in encoding_maps.items():
    if col in df.columns:
        df[col] = df[col].map(mapping)

X = df.drop(target_col, axis=1)
y = df[target_col]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model + scaler
with open("heart_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model and scaler saved!")