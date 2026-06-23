import matplotlib.pyplot as plt
import os


# =====================================================
# SAFE VALUE EXTRACTION
# =====================================================

def safe_extract(results, key):

    values = []

    for r in results:

        if key in r:

            values.append(r[key])

    return values


# =====================================================
# RESEARCH BENCHMARK PLOTS
# =====================================================

def plot_trial_statistics(
    trial_results
):

    os.makedirs(
        "graphs",
        exist_ok=True
    )

    # =================================================
    # SAFE EXTRACTION
    # =================================================

    runs = list(
        range(
            1,
            len(trial_results) + 1
        )
    )

    costs = safe_extract(
        trial_results,
        "cost"
    )

    risks = safe_extract(
        trial_results,
        "risk"
    )

    distances = safe_extract(
        trial_results,
        "distance"
    )

    turns = safe_extract(
        trial_results,
        "turns"
    )

    # =================================================
    # COST STABILITY
    # =================================================

    if len(costs) > 0:

        plt.figure()

        plt.plot(
            runs[:len(costs)],
            costs,
            marker='o'
        )

        plt.title(
            "Cost Stability"
        )

        plt.xlabel("Run")

        plt.ylabel("Cost")

        plt.grid()

        plt.savefig(
            "graphs/cost_stability.png"
        )

        plt.show()

    # =================================================
    # RISK STABILITY
    # =================================================

    if len(risks) > 0:

        plt.figure()

        plt.plot(
            runs[:len(risks)],
            risks,
            marker='o'
        )

        plt.title(
            "Risk Stability"
        )

        plt.xlabel("Run")

        plt.ylabel("Risk")

        plt.grid()

        plt.savefig(
            "graphs/risk_stability.png"
        )

        plt.show()

    # =================================================
    # DISTANCE STABILITY
    # =================================================

    if len(distances) > 0:

        plt.figure()

        plt.plot(
            runs[:len(distances)],
            distances,
            marker='o'
        )

        plt.title(
            "Distance Stability"
        )

        plt.xlabel("Run")

        plt.ylabel("Distance")

        plt.grid()

        plt.savefig(
            "graphs/distance_stability.png"
        )

        plt.show()

    # =================================================
    # TURN STABILITY
    # =================================================

    if len(turns) > 0:

        plt.figure()

        plt.plot(
            runs[:len(turns)],
            turns,
            marker='o'
        )

        plt.title(
            "Turn Stability"
        )

        plt.xlabel("Run")

        plt.ylabel("Turns")

        plt.grid()

        plt.savefig(
            "graphs/turn_stability.png"
        )

        plt.show()