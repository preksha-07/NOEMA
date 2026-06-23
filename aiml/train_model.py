import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("dataset.csv")

# =========================
# FEATURES
# =========================

X = data[
    [
        "distance",
        "turns",
        "vibration"
    ]
]

# =========================
# TARGET
# =========================

y = data["probability"]

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# TRAIN
# =========================

model = LinearRegression()

model.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================

predictions = model.predict(X_test)

mse = mean_squared_error(
    y_test,
    predictions
)

print("MODEL TRAINED")
print("MSE :", round(mse, 5))

# =========================
# SAVE
# =========================

with open("saved_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("saved_model.pkl CREATED")