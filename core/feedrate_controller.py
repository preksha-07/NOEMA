import math


# =====================================================
# ADAPTIVE FEEDRATE
# =====================================================

def compute_feedrate(
    angle,
    base_feedrate=1500
):

    # Sharp turn
    if angle > 2.0:

        return base_feedrate * 0.5

    # Medium turn
    elif angle > 1.0:

        return base_feedrate * 0.75

    # Smooth
    else:

        return base_feedrate