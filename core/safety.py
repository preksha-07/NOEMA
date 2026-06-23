# =====================================================
# MACHINE LIMITS
# =====================================================

MAX_X = 300
MAX_Y = 300

MIN_X = 0
MIN_Y = 0


# =====================================================
# VALIDATE SINGLE COORDINATE
# =====================================================

def validate_coordinate(x, y):

    if x < MIN_X or x > MAX_X:
        return False

    if y < MIN_Y or y > MAX_Y:
        return False

    return True


# =====================================================
# VALIDATE COMMAND
# =====================================================

def validate_command(command):

    try:

        parts = command.split()

        x = None
        y = None

        for part in parts:

            if part.startswith("X"):

                x = float(part[1:])

            elif part.startswith("Y"):

                y = float(part[1:])

        if x is None or y is None:

            return False

        return validate_coordinate(x, y)

    except:

        return False