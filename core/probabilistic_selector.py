import random
import math


# =====================================================
# PROBABILISTIC PATH SELECTION
# =====================================================

def probabilistic_selection(
    results,
    keep_count=10,
    temperature=1000
):

    selected = []

    # -------------------------------------------------
    # Compute probabilities
    # -------------------------------------------------

    energies = [r["energy"] for r in results]

    probabilities = []

    for energy in energies:

        probability = math.exp(
            -energy / max(temperature, 1e-9)
        )

        probabilities.append(probability)

    # Normalize
    total = sum(probabilities)

    probabilities = [
        p / total for p in probabilities
    ]

    # -------------------------------------------------
    # Probabilistic sampling
    # -------------------------------------------------

    selected_indices = random.choices(
        range(len(results)),
        weights=probabilities,
        k=keep_count
    )

    # Remove duplicates
    unique_indices = list(set(selected_indices))

    for idx in unique_indices:

        selected.append(results[idx])

    return selected