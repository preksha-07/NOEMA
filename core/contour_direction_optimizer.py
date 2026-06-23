import math


# =====================================================
# DISTANCE
# =====================================================

def point_distance(p1, p2):

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt(dx**2 + dy**2)


# =====================================================
# OPTIMIZE CONTOUR DIRECTIONS
# =====================================================

def optimize_contour_directions(contours):

    if len(contours) <= 1:
        return contours

    optimized = [contours[0]]

    for i in range(1, len(contours)):

        previous = optimized[-1]

        current = contours[i]

        prev_points = previous["points"]
        curr_points = current["points"]

        # -------------------------------------------------
        # Previous contour END
        # -------------------------------------------------

        prev_end = prev_points[
            previous["path"][-1]
        ]

        # -------------------------------------------------
        # Current normal direction
        # -------------------------------------------------

        normal_start = curr_points[
            current["path"][0]
        ]

        normal_distance = point_distance(
            prev_end,
            normal_start
        )

        # -------------------------------------------------
        # Current reversed direction
        # -------------------------------------------------

        reversed_start = curr_points[
            current["path"][-1]
        ]

        reversed_distance = point_distance(
            prev_end,
            reversed_start
        )

        # -------------------------------------------------
        # Choose better direction
        # -------------------------------------------------

        if reversed_distance < normal_distance:

            current["path"] = list(
                reversed(current["path"])
            )

        optimized.append(current)

    return optimized