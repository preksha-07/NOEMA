import matplotlib.pyplot as plt
import os

# =====================================================
# CREATE GRAPHS FOLDER
# =====================================================

os.makedirs(
    "graphs",
    exist_ok=True
)

# =====================================================
# PLOT POINTS
# =====================================================

def plot_points(points):

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    plt.figure()

    plt.scatter(x, y)

    plt.title("Extracted Points")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.grid()

    plt.gca().invert_yaxis()

    plt.savefig(
        "graphs/extracted_points.png"
    )

    plt.close()


# =====================================================
# PLOT PATH
# =====================================================

def plot_path(
    points,
    path,
    title="Path",
    filename=None
):

    x = [points[i][0] for i in path]
    y = [points[i][1] for i in path]

    # close loop
    x.append(points[path[0]][0])
    y.append(points[path[0]][1])

    plt.figure()

    plt.plot(
        x,
        y,
        marker="o"
    )

    plt.title(title)

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.grid()

    plt.gca().invert_yaxis()

    if filename:

        plt.savefig(
            f"graphs/{filename}"
        )

    plt.close()


# =====================================================
# COMPARE PATHS
# =====================================================

def compare_paths(
    points,
    random_path,
    best_path
):

    plt.figure()

    # Classical
    x1 = [points[i][0] for i in random_path]
    y1 = [points[i][1] for i in random_path]

    x1.append(points[random_path[0]][0])
    y1.append(points[random_path[0]][1])

    # Optimized
    x2 = [points[i][0] for i in best_path]
    y2 = [points[i][1] for i in best_path]

    x2.append(points[best_path[0]][0])
    y2.append(points[best_path[0]][1])

    plt.plot(
        x1,
        y1,
        "r--",
        marker="o",
        label="Classical"
    )

    plt.plot(
        x2,
        y2,
        "g-",
        marker="o",
        label="Optimized"
    )

    plt.title("Path Comparison")

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.legend()

    plt.grid()

    plt.gca().invert_yaxis()

    plt.savefig(
        "graphs/path_comparison.png"
    )

    plt.close()