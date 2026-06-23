import matplotlib.pyplot as plt
import numpy as np
import json

def plot_prediction_vs_actual(predicted, actual):
    labels = ['Time', 'Risk', 'Cost']

    predicted_values = [
        predicted['time'],
        predicted['risk'],
        predicted['cost']
    ]

    actual_values = [
        actual['time'],
        actual['risk'],
        actual['cost']
    ]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure()

    plt.bar(x - width/2, predicted_values, width, label='Predicted')
    plt.bar(x + width/2, actual_values, width, label='Actual')

    plt.xticks(x, labels)
    plt.title("Digital Twin: Predicted vs Actual")
    plt.ylabel("Value")

    plt.legend()
    plt.grid(axis='y')

    # Add values on top
    for i, v in enumerate(predicted_values):
        plt.text(i - width/2, v + 2, str(round(v, 2)), ha='center')

    for i, v in enumerate(actual_values):
        plt.text(i + width/2, v + 2, str(round(v, 2)), ha='center')
    

    plt.savefig(
    "graphs/digital_twin.png"
)
    plt.close()


def plot_learning_curve(log_file="data/logs.json"):

    with open(log_file, "r") as f:
        data = json.load(f)


    error_cost = []
    error_risk = []

    for entry in data:
        if "error_cost" in entry and "error_risk" in entry:
            error_cost.append(entry["error_cost"])
            error_risk.append(entry["error_risk"])

  
    if len(error_cost) == 0:
        print("No valid learning data found.")
        return
    
    
    min_len = min(len(error_cost), len(error_risk))
    iterations = list(range(1, min_len + 1))

    plt.figure()

    plt.plot(iterations, error_cost, label="Cost Error")
    plt.plot(iterations, error_risk, label="Risk Error")

    plt.xlabel("Run Number")
    plt.ylabel("Error")

    plt.title("Learning Curve (System Improvement)")
    plt.legend()
    plt.grid()

    plt.savefig(
         "graphs/learning_curve.png"
    )

    plt.close()

def plot_cost_stability(results):

    runs = [
        r["run"]
        for r in results
    ]

    costs = [
        r["cost"]
        for r in results
    ]

    plt.figure()

    plt.plot(
        runs,
        costs,
        marker="o"
    )

    plt.title("Cost Stability")

    plt.xlabel("Run")

    plt.ylabel("Cost")

    plt.grid()

    plt.savefig(
        "graphs/cost_stability.png"
    )

    plt.close()

def plot_risk_stability(results):

    runs = [r["run"] for r in results]

    risks = [r["risk"] for r in results]

    plt.figure()

    plt.plot(
        runs,
        risks,
        marker="o"
    )

    plt.title("Risk Stability")

    plt.xlabel("Run")

    plt.ylabel("Risk")

    plt.grid()

    plt.savefig(
        "graphs/risk_stability.png"
    )

    plt.close()

def plot_distance_stability(results):

    runs = [r["run"] for r in results]

    distances = [
        r["distance"]
        for r in results
    ]

    plt.figure()

    plt.plot(
        runs,
        distances,
        marker="o"
    )

    plt.title("Distance Stability")

    plt.xlabel("Run")

    plt.ylabel("Distance")

    plt.grid()

    plt.savefig(
        "graphs/distance_stability.png"
    )

    plt.close()

def plot_turn_stability(results):

    runs = [r["run"] for r in results]

    turns = [
        r["turns"]
        for r in results
    ]

    plt.figure()

    plt.plot(
        runs,
        turns,
        marker="o"
    )

    plt.title("Turn Stability")

    plt.xlabel("Run")

    plt.ylabel("Turns")

    plt.grid()

    plt.savefig(
        "graphs/turn_stability.png"
    )

    plt.close()