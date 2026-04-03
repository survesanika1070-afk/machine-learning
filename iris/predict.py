import pickle

# Load model
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

# Take input
sepal_length = float(input("Sepal Length: "))
sepal_width = float(input("Sepal Width: "))
petal_length = float(input("Petal Length: "))
petal_width = float(input("Petal Width: "))

# Prediction
prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

# Output label mapping
labels = ["Setosa", "Versicolor", "Virginica"]

print("Predicted Flower:", labels[prediction[0]])