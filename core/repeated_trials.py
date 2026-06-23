from core.solver import advanced_solver
from core.metrics import (
    compute_cost,
    compute_risk,
    estimate_speed
)
from core.qubo import compute_energy


# =====================================================
# REPEATED TRIALS
# =====================================================

def run_trials(
    points,
    Q,
    candidate,
    runs=5,
    mode="balanced",
    risk_weight=1.0
):

    results = []

    for i in range(runs):

        path, cost = advanced_solver(
            points,
            Q,
            initial_path=candidate,
            iterations=5000,
            T=500,
            mode=mode,
            risk_weight=risk_weight
        )

        distance = compute_energy(path, Q)

        speed = estimate_speed(distance)

        risk = compute_risk(
            points,
            path,
            speed
        )

        results.append({

            "run": i + 1,

            "path": path,

            "cost": cost,

            "distance": distance,

            "risk": risk
        })

    return results