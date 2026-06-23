# core/predictor.py

from core.metrics import estimate_time, compute_risk


def predict_metrics(distance, turns, mode):
    """
    Predict system behavior BEFORE execution
    """

    # -------------------------------
    # 1. Estimate speed based on mode
    # -------------------------------
    speed = 1.0

    if mode == "speed":
        speed = 1.5
    elif mode == "accuracy":
        speed = 0.7

    # -------------------------------
    # 2. Predict time
    # -------------------------------
    predicted_time = estimate_time(distance, speed)

    # -------------------------------
    # 3. Predict risk
    # -------------------------------
    predicted_risk = turns * speed * 2.0

    # -------------------------------
    # 4. Predict cost (CORRECT METHOD)
    # -------------------------------
    if mode == "speed":
        w1, w2, w3 = 0.5, 1.5, 0.5
    elif mode == "accuracy":
        w1, w2, w3 = 1.0, 0.5, 1.5
    else:
        w1, w2, w3 = 1.0, 1.0, 1.0

    predicted_cost = distance + (w3 * predicted_risk)

    # -------------------------------
    # 5. Return prediction
    # -------------------------------
    return {
        "time": predicted_time,
        "risk": predicted_risk,
        "cost": predicted_cost,
        "speed": speed
    }