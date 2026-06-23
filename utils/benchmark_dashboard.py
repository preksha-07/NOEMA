import matplotlib.pyplot as plt


# =====================================================
# FULL BENCHMARK DASHBOARD
# =====================================================

def benchmark_dashboard(
    classical,
    optimized,
    predicted
):

    labels = [
        "Distance",
        "Risk",
        "Cost"
    ]

    classical_values = [
        classical["distance"],
        classical["risk"],
        classical["cost"]
    ]

    optimized_values = [
        optimized["distance"],
        optimized["risk"],
        optimized["cost"]
    ]

    predicted_values = [
        predicted["time"],
        predicted["risk"],
        predicted["cost"]
    ]

    # -------------------------------------------------
    # COMPARISON
    # -------------------------------------------------

    plt.figure()

    plt.plot(
        labels,
        classical_values,
        marker='o',
        label="Classical"
    )

    plt.plot(
        labels,
        optimized_values,
        marker='o',
        label="Optimized"
    )

    plt.plot(
        labels,
        predicted_values,
        marker='o',
        label="Predicted"
    )

    plt.title(
        "System Benchmark Dashboard"
    )

    plt.legend()

    plt.grid()

    plt.show()