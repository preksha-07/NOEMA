import pickle
import numpy as np
import os

# =========================
# LOAD TRAINED MODEL
# =========================

trained_model = None
MODEL_LOADED = False



try:

    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "saved_model.pkl"
    )

    with open(
        MODEL_PATH,
        "rb"
    ) as f:

        trained_model = pickle.load(f)

    MODEL_LOADED = True

    print("AIML MODEL LOADED SUCCESSFULLY")

except Exception as e:

    print("AIML MODEL FAILED TO LOAD")
    print(e)

    trained_model = None
    MODEL_LOADED = False

# =========================
# MAIN PREDICTION
# =========================

def predict(
    distance,
    turns,
    vibration
):

    if not MODEL_LOADED:

        return 0.5

    features = np.array([
        [
            distance,
            turns,
            vibration
        ]
    ])

    raw_output = trained_model.predict(
    features
)[0]

    print("MODEL INPUT:", features)
    print("RAW MODEL OUTPUT:", raw_output)

    probability = 1 / (
    1 + np.exp(-raw_output)
)

    print("PROBABILITY:", probability)

    return round(
        float(probability),
        4
    )


# =========================
# RISK LEVEL
# =========================

def risk_level(
    probability
):

    if probability >= 0.80:

        return "HIGH"

    elif probability >= 0.60:

        return "MEDIUM"

    else:

        return "LOW"


# =========================
# FUTURE RISK
# =========================

def future_risk(
    probability,
    vibration
):

    future = probability + (
        vibration / 1000
    )

    future = min(
        future,
        1.0
    )

    return round(
        future,
        4
    )


# =========================
# RECOMMENDATIONS
# =========================

def recommendations(
    probability,
    vibration
):

    rec = []

    if probability >= 0.80:

        rec.append(
            "Immediate maintenance recommended"
        )

    elif probability >= 0.60:

        rec.append(
            "Schedule maintenance"
        )

    if vibration > 60:

        rec.append(
            "Inspect machine vibration"
        )

    if vibration > 80:

        rec.append(
            "Check spindle alignment"
        )

    if len(rec) == 0:

        rec.append(
            "System operating normally"
        )

    return rec