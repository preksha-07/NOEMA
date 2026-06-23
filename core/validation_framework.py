import json
import os

from core.metrics import (
    compute_cost,
    compute_risk,
    count_turns
)

from core.qubo import compute_energy


# =====================================================
# RUN EXPERIMENT
# =====================================================

def run_experiment(
    points,
    Q,
    path,
    mode,
    risk_weight
):

    distance = compute_energy(path, Q)

    turns = count_turns(points, path)

    risk = compute_risk(
        points,
        path,
        distance
    )

    cost = compute_cost(
        points,
        path,
        Q,
        mode,
        risk_weight
    )

    return {
        "distance": distance,
        "turns": turns,
        "risk": risk,
        "cost": cost
    }


# =====================================================
# COMPARE RESULTS
# =====================================================

def compare_results(classical, optimized):

    improvement = (
        (
            classical["cost"]
            - optimized["cost"]
        )
        /
        classical["cost"]
    ) * 100

    return {
        "improvement_percent": improvement
    }


# =====================================================
# GENERATE REPORT
# =====================================================

def generate_report(
    data,
    filename="experiments/report.json"
):

    os.makedirs(
        "experiments",
        exist_ok=True
    )

    with open(filename, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

    print(
        "\nReport saved:",
        filename
    )