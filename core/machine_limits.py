# =====================================================
# MACHINE LIMIT CHECKER
# =====================================================

def enforce_machine_limits(
    toolpath,
    max_x=200,
    max_y=200
):

    safe_toolpath = []

    for segment in toolpath:

        safe_segment = []

        for x, y in segment:

            x = max(0, min(x, max_x))
            y = max(0, min(y, max_y))

            safe_segment.append((x, y))

        safe_toolpath.append(safe_segment)

    return safe_toolpath