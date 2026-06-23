import os


# =====================================================
# SAVE G-CODE FILE
# =====================================================

def save_gcode(
    gcode,
    filename="output.gcode"
):

    os.makedirs(
        "gcode",
        exist_ok=True
    )

    path = os.path.join(
        "gcode",
        filename
    )

    with open(path, "w") as f:

        for line in gcode:

            f.write(line + "\n")

    print(
        f"\nG-code saved to: {path}"
    )