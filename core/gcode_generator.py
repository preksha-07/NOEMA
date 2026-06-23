from core.feedrate_controller import (
    compute_feedrate
)
from core.metrics import pixels_to_mm

import math


# =====================================================
# ANGLE CALCULATION
# =====================================================

def segment_angle(p1, p2, p3):

    v1 = (
        p2[0] - p1[0],
        p2[1] - p1[1]
    )

    v2 = (
        p3[0] - p2[0],
        p3[1] - p2[1]
    )

    mag1 = math.sqrt(
        v1[0] ** 2 +
        v1[1] ** 2
    )

    mag2 = math.sqrt(
        v2[0] ** 2 +
        v2[1] ** 2
    )

    if mag1 == 0 or mag2 == 0:
        return 0

    dot = (
        v1[0] * v2[0]
        + v1[1] * v2[1]
    )

    cos_theta = dot / (mag1 * mag2)

    cos_theta = max(
        -1,
        min(1, cos_theta)
    )

    return math.acos(cos_theta)


# =====================================================
# GENERATE G-CODE FROM TOOLPATH
# =====================================================

def generate_gcode(
    toolpath,
    feedrate=1500,
    draw_z=-1,
    travel_z=5
):

    gcode = []

    # =====================================
# AUTO SCALE TO 300mm WORKSPACE
# =====================================

    max_coordinate = 1

    for segment in toolpath:
        for x, y in segment:
            max_coordinate = max(
            max_coordinate,
            x,
            y
        )

    scale = 150 / max_coordinate

    print(
    "GCODE SCALE:",
    scale
)

    # -------------------------------------------------
    # INITIALIZATION
    # -------------------------------------------------

    gcode.append(
        "G21 ; Set units to mm"
    )

    gcode.append(
        "G90 ; Absolute positioning"
    )

    # -------------------------------------------------
    # PROCESS EACH SEGMENT
    # -------------------------------------------------

    for segment in toolpath:

        if not segment:
            continue

        start_x, start_y = segment[0]
        
        start_x = pixels_to_mm(start_x)
        start_y = pixels_to_mm(start_y)

        start_x *= scale
        start_y *= scale

        # ---------------------------------------------
        # PEN UP + RAPID MOVE
        # ---------------------------------------------

        gcode.append(
            f"G00 Z{travel_z}"
        )

        gcode.append(
            f"G00 X{start_x:.2f} Y{start_y:.2f}"
        )

        # ---------------------------------------------
        # PEN DOWN
        # ---------------------------------------------

        gcode.append(
            f"G01 Z{draw_z}"
        )

        # ---------------------------------------------
        # DRAW WITH ADAPTIVE FEEDRATE
        # ---------------------------------------------

        for i in range(len(segment)):

            x, y = segment[i]

            x = pixels_to_mm(x)
            y = pixels_to_mm(y)

            x *= scale
            y *= scale

            current_feedrate = feedrate

            if (
                i > 0 and
                i < len(segment) - 1
            ):

                angle = segment_angle(
                    segment[i - 1],
                    segment[i],
                    segment[i + 1]
                )

                current_feedrate = compute_feedrate(
                    angle,
                    feedrate
                )

            gcode.append(
                f"G01 X{x:.2f} Y{y:.2f} F{int(current_feedrate)}"
            )

        # ---------------------------------------------
        # PEN UP
        # ---------------------------------------------

        gcode.append(
            "M05 ; Pen up"
        )

    return gcode