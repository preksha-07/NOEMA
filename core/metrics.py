import math
from .qubo import compute_energy


# =====================================================
# MACHINE CALIBRATION
# =====================================================

PLATE_SIZE_MM = 300      # 30 cm
IMAGE_SIZE_PX = 500      # typical image width

MM_PER_PIXEL = (
    PLATE_SIZE_MM /
    IMAGE_SIZE_PX
)

def pixels_to_mm(distance_pixels):

    return (
        distance_pixels *
        MM_PER_PIXEL
    )


# =====================================================
# BASIC METRICS
# =====================================================

def count_moves(path):
    return len(path)


def estimate_time(
    distance_pixels,
    speed_mm_per_sec=50
):

    distance_mm = (
        distance_pixels *
        MM_PER_PIXEL
    )

    return (
        distance_mm /
        speed_mm_per_sec
    )


def estimate_speed(distance, base_speed=1.0):
    # simple proportional model
    return base_speed + 0.01 * distance


# =====================================================
# TURN CALCULATION
# =====================================================

def count_turns(points, path):
    turns = 0

    for i in range(1, len(path) - 1):
        p1 = points[path[i - 1]]
        p2 = points[path[i]]
        p3 = points[path[i + 1]]

        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])

        if v1 != v2:
            turns += 1

    return turns


def compute_turn_angles(points, path):
    angles = []

    for i in range(1, len(path) - 1):
        p1 = points[path[i - 1]]
        p2 = points[path[i]]
        p3 = points[path[i + 1]]

        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])

        dot = v1[0]*v2[0] + v1[1]*v2[1]

        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)

        if mag1 == 0 or mag2 == 0:
            continue

        cos_angle = dot / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # numerical safety

        angle = math.acos(cos_angle)
        angles.append(angle)

    return angles


# =====================================================
# RISK MODEL
# =====================================================

def compute_risk(points, path, speed, vibration=0):
    angles = compute_turn_angles(points, path)

    angle_risk = sum(angles)  # sharper = larger total

    a = 1.0   # angle importance
    b = 0.5   # speed importance
    c = 0.2   # vibration (future)

    return a * angle_risk + b * speed + c * vibration

# =====================================================
# CONSTRAINT PENALTIES
# =====================================================

def sharp_turn_penalty(points, path, threshold=2.5):
    angles = compute_turn_angles(points, path)
    return sum(1 for angle in angles if angle > threshold)


def smoothness_penalty(points, path):
    angles = compute_turn_angles(points, path)

    if len(angles) < 2:
        return 0

    return sum(abs(angles[i+1] - angles[i]) for i in range(len(angles) - 1))


def speed_penalty(distance, max_speed=100):
    if distance > max_speed:
        return (distance - max_speed) * 0.1
    return 0


# =====================================================
# MODE WEIGHTS
# =====================================================

def get_weights(mode="balanced"):
    if mode == "speed":
        return {
            "distance": 1.0,
            "risk": 0.2,
            "turns": 0.2,
            "smoothness": 0.2,
            "speed": 1.5
        }

    elif mode == "accuracy":
        return {
            "distance": 0.5,
            "risk": 1.5,
            "turns": 1.5,
            "smoothness": 1.5,
            "speed": 0.5
        }

    else:  # balanced
        return {
            "distance": 1.0,
            "risk": 1.0,
            "turns": 1.0,
            "smoothness": 1.0,
            "speed": 1.0
        }


# =====================================================
# FINAL COST FUNCTION (MAIN)
# =====================================================

def compute_cost(points, path, Q, mode="balanced", risk_weight=1.0,vibration=0):

    weights = get_weights(mode)

    # =====================================================
    # DISTANCE
    # =====================================================

    distance = compute_energy(path, Q)

    # =====================================================
    # DERIVED METRICS
    # =====================================================

    turns = count_turns(points, path)

    speed = estimate_speed(distance)
    time_est = estimate_time(distance)

    # =====================================================
    # RISK
    # =====================================================

    risk = compute_risk(points, path, speed,vibration)

    # =====================================================
    # CONSTRAINT PENALTIES
    # =====================================================

    turns_pen = sharp_turn_penalty(points, path)

    smooth_pen = smoothness_penalty(points, path)

    speed_pen = speed_penalty(distance)

    # =====================================================
    # JUMP PENALTY
    # =====================================================

    jump_penalty = 0

    for i in range(len(path) - 1):

        p1 = points[path[i]]
        p2 = points[path[i + 1]]

        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]

        jump_distance = (dx**2 + dy**2) ** 0.5

        # Penalize large jumps
        if jump_distance > 80:

            jump_penalty += jump_distance * 2

    # =====================================================
    # FINAL COST
    # =====================================================

    total_cost = (
        weights["distance"] * distance +
        0.5 * time_est +
        weights["risk"] * risk_weight * risk +
        weights["turns"] * turns_pen +
        weights["smoothness"] * smooth_pen +
        weights["speed"] * speed_pen +
        jump_penalty
    )

    return total_cost