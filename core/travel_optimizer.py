import math


# =====================================================
# DISTANCE
# =====================================================

def point_distance(p1, p2):

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt(dx**2 + dy**2)


# =====================================================
# COMPUTE TRAVEL METRICS
# =====================================================

def compute_travel_metrics(toolpath):

    if len(toolpath) <= 1:

        return {
            "travel_distance": 0,
            "travel_moves": 0,
            "travel_time": 0
        }

    total_distance = 0

    travel_moves = 0

    for i in range(len(toolpath) - 1):

        current_segment = toolpath[i]
        next_segment = toolpath[i + 1]

        if not current_segment or not next_segment:
            continue

        current_end = current_segment[-1]
        next_start = next_segment[0]

        dx = current_end[0] - next_start[0]
        dy = current_end[1] - next_start[1]

        distance = math.sqrt(dx**2 + dy**2)

        total_distance += distance

        travel_moves += 1

    travel_time = total_distance / 3000

    return {
        "travel_distance": total_distance,
        "travel_moves": travel_moves,
        "travel_time": travel_time
    }