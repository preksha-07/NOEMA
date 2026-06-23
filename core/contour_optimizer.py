from .qubo import build_qubo
from .metrics import compute_cost
from .solver import advanced_solver

def optimize_contours(
    contours,
    mode="balanced",
    risk_weight=1.0
):

    optimized_contours = []

    for contour in contours:

        if len(contour) < 5:
            continue

        Q = build_qubo(contour)

        initial_path = list(range(len(contour)))

        best_path, best_cost = advanced_solver(

            contour,

            Q,

            initial_path=initial_path,

            iterations=5000,

            T=500,

            mode=mode,

            risk_weight=risk_weight
        )

        optimized_contours.append({

    "points": contour,

    "path": best_path,

    "cost": best_cost
})

    return optimized_contours