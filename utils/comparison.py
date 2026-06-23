import matplotlib.pyplot as plt

def plot_cost_comparison(random_cost, optimized_cost, predicted_cost):
    labels = ['Random', 'Optimized', 'Predicted']
    values = [random_cost, optimized_cost, predicted_cost]

    plt.figure()
    plt.bar(labels, values)

    plt.title("Cost Comparison")
    plt.ylabel("Cost Value")

    for i, v in enumerate(values):
        plt.text(i, v + 5, str(round(v, 2)), ha='center')

    plt.grid(axis='y')
    plt.savefig(
    "graphs/cost_comparison.png"
)
    plt.show()
