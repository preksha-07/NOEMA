# =========================
# IMPORTS
# =========================

import json
from datetime import datetime

from model import (
    predict,
    risk_level,
    future_risk,
    recommendations,
    MODEL_LOADED
)

from esp32_data import (
    get_esp32_data
)

# =========================
# MODEL STATUS
# =========================

print(f"MODEL LOADED = {MODEL_LOADED}")

# =========================
# GET ESP32 DATA
# =========================

sensor_data = get_esp32_data()

# =========================
# ESP32 CHECK
# =========================

if sensor_data is None:

    print("ESP32 NOT CONNECTED")

    distance = 0
    turns = 0
    vibration = 0

else:

    print("ESP32 CONNECTED")

    distance = sensor_data["distance"]
    turns = sensor_data["turns"]
    vibration = sensor_data["vibration"]

# =========================
# AI PREDICTION
# =========================

probability = predict(
    distance,
    turns,
    vibration
)

risk = risk_level(
    probability
)

future = future_risk(
    probability,
    vibration
)

rec = recommendations(
    probability,
    vibration
)

# =========================
# DISPLAY RESULTS
# =========================

print()
print("========== AIML RESULT ==========")
print()

print(f"Distance       : {distance}")
print(f"Turns          : {turns}")
print(f"Vibration      : {vibration}")
print(f"Probability    : {probability}")
print(f"Risk Level     : {risk}")
print(f"Future Risk    : {future}")

print()
print("Recommendations")

for r in rec:

    print("-", r)

# =========================
# RESULT OBJECT
# =========================

result = {

    "distance": distance,
    "turns": turns,
    "vibration": vibration,
    "probability": probability,
    "risk": risk,
    "future_risk": future,
    "recommendations": rec
}

# =========================
# DIGITAL TWIN LOG
# =========================

log_entry = {

    "timestamp":
    str(
        datetime.now()
    ),

    "distance":
    distance,

    "turns":
    turns,

    "vibration":
    vibration,

    "probability":
    probability,

    "risk":
    risk,

    "future_risk":
    future
}

with open(
    "digital_twin_logs.txt",
    "a"
) as file:

    file.write(
        json.dumps(
            log_entry
        )
    )

    file.write("\n")