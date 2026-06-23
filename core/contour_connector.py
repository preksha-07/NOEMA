import math


# =====================================================
# DISTANCE
# =====================================================

def point_distance(p1, p2):

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt(dx**2 + dy**2)


# =====================================================
# ROTATE PATH
# =====================================================

def rotate_path(path, start_idx):

    return (
        path[start_idx:]
        + path[:start_idx]
    )


# =====================================================
# FIND BEST ENTRY POINT
# =====================================================

def best_entry_point(
    previous_end,
    points,
    path
):

    best_distance = float("inf")
    best_rotation = path

    for i in range(len(path)):

        rotated = rotate_path(path, i)

        start_point = points[rotated[0]]

        d = point_distance(
            previous_end,
            start_point
        )

        if d < best_distance:

            best_distance = d
            best_rotation = rotated

    return best_rotation


# =====================================================
# CONNECT CONTOURS
# =====================================================

def connect_contours(optimized_contours):

    if not optimized_contours:
        return [], []

    final_points = []
    final_path = []

    point_offset = 0

    previous_end = None

    for contour_data in optimized_contours:

        points = contour_data["points"]
        path = contour_data["path"]

        # -------------------------------------------------
        # OPTIMIZE ENTRY POINT
        # -------------------------------------------------

        if previous_end is not None:

            path = best_entry_point(
                previous_end,
                points,
                path
            )

        # -------------------------------------------------
        # STORE UPDATED PATH
        # -------------------------------------------------

        contour_data["path"] = path

        # -------------------------------------------------
        # ADD POINTS
        # -------------------------------------------------

        final_points.extend(points)

        adjusted_path = [
            p + point_offset
            for p in path
        ]

        final_path.extend(adjusted_path)

        # -------------------------------------------------
        # UPDATE END POINT
        # -------------------------------------------------

        previous_end = points[path[-1]]

        point_offset += len(points)

    return final_points, final_path