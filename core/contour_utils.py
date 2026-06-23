import cv2


# =====================================================
# EXTRACT CONTOURS
# =====================================================

def extract_contours(edges):

    result = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    contours = result[0] if len(result) == 2 else result[1]

    contour_groups = []

    for contour in contours:

        points = []

        for p in contour:

            x, y = p[0]

            points.append((int(x), int(y)))

        contour_groups.append(points)

    return contour_groups


# =====================================================
# REMOVE DUPLICATES
# =====================================================

def clean_contour(points):

    cleaned = []

    for p in points:

        if p not in cleaned:
            cleaned.append(p)

    return cleaned


# =====================================================
# REDUCE POINT COUNT
# =====================================================

def reduce_contour(points, max_points=80):

    if len(points) <= max_points:
        return points

    step = len(points) // max_points

    return points[::step]