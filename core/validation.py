import statistics
import random

from core.qubo import compute_energy

from core.metrics import (
    compute_risk,
    count_turns,
    estimate_speed
)

from core.solver import advanced_solver


# =====================================================
# MULTI-RUN VALIDATION
# =====================================================

def run_trials(
    points,
    Q,
    base_path,
    runs=5,
    mode="balanced",
    risk_weight=1.0
):

    results = []

    for i in range(runs):

        # =============================================
        # RANDOMIZE STARTING PATH
        # =============================================

        random_path = base_path.copy()
        

        # =============================================
        # OPTIMIZATION
        # =============================================

        path, cost = advanced_solver(

            points,
            Q,

            initial_path=random_path,

            iterations=2000,

            T=500,

            mode=mode,

            risk_weight=risk_weight
        )

        # =============================================
        # METRICS
        # =============================================

        distance = compute_energy(
            path,
            Q
        )

        turns = count_turns(
            points,
            path
        )

        speed = estimate_speed(
            distance
        )

        risk = compute_risk(
            points,
            path,
            speed
        )

        # =============================================
        # STORE RESULTS
        # =============================================

        result = {

            "run": i + 1,

            "distance": float(distance),

            "turns": int(turns),

            "risk": float(risk),

            "cost": float(cost)
        }

        results.append(result)

    return results


# =====================================================
# VALIDATE RESULTS
# =====================================================

def validate_runs(results):

    cleaned_results = []

    for r in results:

        if (
            "cost" in r and
            "risk" in r and
            "distance" in r and
            "turns" in r
        ):

            cleaned_results.append(r)

    if len(cleaned_results) == 0:

        return {

            "cost_mean": 0,
            "cost_std": 0,

            "risk_mean": 0,
            "risk_std": 0,

            "distance_mean": 0,
            "distance_std": 0,

            "turn_mean": 0,
            "turn_std": 0
        }

    costs = [r["cost"] for r in cleaned_results]
    risks = [r["risk"] for r in cleaned_results]
    distances = [r["distance"] for r in cleaned_results]
    turns = [r["turns"] for r in cleaned_results]

    return {

        "cost_mean":
            statistics.mean(costs),

        "cost_std":
            statistics.stdev(costs)
            if len(costs) > 1 else 0,

        "risk_mean":
            statistics.mean(risks),

        "risk_std":
            statistics.stdev(risks)
            if len(risks) > 1 else 0,

        "distance_mean":
            statistics.mean(distances),

        "distance_std":
            statistics.stdev(distances)
            if len(distances) > 1 else 0,

        "turn_mean":
            statistics.mean(turns),

        "turn_std":
            statistics.stdev(turns)
            if len(turns) > 1 else 0
    }