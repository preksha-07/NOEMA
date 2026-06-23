import math
import random


# =====================================================
# DISTANCE BETWEEN POINTS
# =====================================================

def point_distance(p1, p2):

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt(dx**2 + dy**2)


# =====================================================
# CONTOUR CENTER
# =====================================================

def contour_center(contour_points):

    x = sum(p[0] for p in contour_points) / len(contour_points)
    y = sum(p[1] for p in contour_points) / len(contour_points)

    return (x, y)


# =====================================================
# TOTAL INTER-CONTOUR TRAVEL
# =====================================================

def contour_order_cost(contours, order):

    total = 0

    for i in range(len(order) - 1):

        c1 = contours[order[i]]["points"]
        c2 = contours[order[i + 1]]["points"]

        center1 = contour_center(c1)
        center2 = contour_center(c2)

        total += point_distance(center1, center2)

    return total


# =====================================================
# SIMPLE ORDER OPTIMIZER
# =====================================================

def optimize_contour_order(contours, iterations=2000):

    if len(contours) <= 1:
        return contours

    current_order = list(range(len(contours)))
    random.shuffle(current_order)

    best_order = current_order.copy()

    best_cost = contour_order_cost(
        contours,
        best_order
    )

    for _ in range(iterations):

        new_order = current_order.copy()

        i, j = random.sample(
            range(len(new_order)),
            2
        )

        new_order[i], new_order[j] = (
            new_order[j],
            new_order[i]
        )

        new_cost = contour_order_cost(
            contours,
            new_order
        )

        if new_cost < best_cost:

            best_order = new_order
            best_cost = new_cost

            current_order = new_order

    optimized = [
        contours[i]
        for i in best_order
    ]

    return optimized