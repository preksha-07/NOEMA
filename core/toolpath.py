# =====================================================
# BUILD TOOLPATH SEGMENTS
# =====================================================

def build_toolpath(optimized_contours):

    toolpath = []

    for contour_data in optimized_contours:

        points = contour_data["points"]
        path = contour_data["path"]

        segment = []

        for idx in path:

            segment.append(points[idx])

        toolpath.append(segment)

    return toolpath