from core.pipeline import run_pipeline

from core.metrics import (
    count_turns,
    compute_risk,
    estimate_speed
)

from core.qubo import (
    build_qubo,
    compute_energy
)

from aiml.model import (
    predict,
    risk_level,
    future_risk,
    recommendations
)


# =====================================================
# FULL PIPELINE + METRICS
# =====================================================

def run_full_pipeline(
    image_path,
    mode="balanced",
    risk_weight=1.0
):

    result = run_pipeline(
        image_path,
        mode,
        risk_weight
    )

    print("CONTOURS:", len(result["contours"]))

    total_distance = 0
    total_turns = 0
    total_risk = 0
    total_cost = 0

    # =============================================
    # PROCESS EACH CONTOUR
    # =============================================

    for contour_data in result["contours"]:

        points = contour_data["points"]
        path = contour_data["path"]

        contour_cost = contour_data["cost"]

        Q = build_qubo(points)

        contour_distance = compute_energy(
            path,
            Q
        )

        contour_turns = count_turns(
            points,
            path
        )

        speed = estimate_speed(
            contour_distance
        )

        contour_risk = compute_risk(
            points,
            path,
            speed
        )

        print(
            "Contour:",
            contour_distance,
            contour_turns,
            contour_risk,
            contour_cost
        )

        total_distance += contour_distance
        total_turns += contour_turns
        total_risk += contour_risk
        total_cost += contour_cost

    # =============================================
    # DEBUG
    # =============================================

    print("\nDEBUG")
    print("Distance:", total_distance)
    print("Turns:", total_turns)
    print("Risk:", total_risk)
    print("Cost:", total_cost)

    # =============================================
    # AIML
    # =============================================

    distance_ai = total_distance

    turns_ai = total_turns

    # Temporary until ESP32 arrives
    vibration_ai = total_risk

    probability = predict(
        distance_ai,
        turns_ai,
        vibration_ai
    )

    risk_ai = risk_level(
        probability
    )

    future_ai = future_risk(
        probability,
        vibration_ai
    )

    recommendation_ai = recommendations(
        probability,
        vibration_ai
    )

    # =============================================
    # RETURN RESULTS
    # =============================================

    return {

        "contours":
            result["total_contours"],

        "segments":
            result["total_segments"],

        "gcode_lines":
            result["gcode_lines"],

        "distance":
            round(total_distance, 2),

        "turns":
            total_turns,

        "risk":
            round(total_risk, 2),

        "cost":
            round(total_cost, 2),

        "probability":
            probability,

        "risk_level":
            risk_ai,

        "future_risk":
            future_ai,

        "recommendations":
            recommendation_ai,

        "gcode":
            result["gcode"]
    }