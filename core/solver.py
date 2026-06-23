import random
import math
from .metrics import compute_cost


# =====================================================
# 2-OPT SWAP
# =====================================================

def two_opt_swap(path):
    new_path = path.copy()

    i = random.randint(0, len(path) - 2)
    j = random.randint(i + 1, len(path) - 1)

    new_path[i:j] = reversed(new_path[i:j])

    return new_path


# =====================================================
# ADVANCED SOLVER (FINAL - FIXED)
# =====================================================

def advanced_solver(
    points,
    Q,
    initial_path=None,
    iterations=5000,
    T=500,
    mode="balanced",
    risk_weight=1.0   # ✅ ADD THIS
):

    # -------------------------------
    # Initial path
    # -------------------------------
    if initial_path is None:
        current_path = list(range(len(points)))
        random.shuffle(current_path)
    else:
        current_path = initial_path.copy()

    # -------------------------------
    # Initial cost (WITH risk_weight)
    # -------------------------------
    current_cost = compute_cost(points, current_path, Q, mode, risk_weight)

    best_path = current_path.copy()
    best_cost = current_cost

    # -------------------------------
    # Optimization loop
    # -------------------------------
    for _ in range(iterations):

        new_path = two_opt_swap(current_path)

        # ✅ FIX: pass risk_weight here too
        new_cost = compute_cost(points, new_path, Q, mode, risk_weight)

        delta = new_cost - current_cost

        # -------------------------------
        # Simulated Annealing Decision
        # -------------------------------
        if delta < 0:
            accept = True
        else:
            try:
                probability = math.exp(-delta / max(T, 1e-9))
            except OverflowError:
                probability = 0

            accept = random.random() < probability

        if accept:
            current_path = new_path
            current_cost = new_cost

        # -------------------------------
        # Update best solution
        # -------------------------------
        if current_cost < best_cost:
            best_path = current_path.copy()
            best_cost = current_cost

        # -------------------------------
        # Cooling schedule
        # -------------------------------
        T = max(T * 0.999, 1e-6)

    return best_path, best_cost