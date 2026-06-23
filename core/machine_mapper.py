# =====================================================
# MACHINE COORDINATE MAPPER
# =====================================================

def map_to_machine_space(
    toolpath,
    machine_width=300,
    machine_height=300
):

    # -------------------------------------------------
    # FIND IMAGE BOUNDS
    # -------------------------------------------------

    all_x = []
    all_y = []

    for segment in toolpath:

        for x, y in segment:

            all_x.append(x)
            all_y.append(y)

    min_x = min(all_x)
    max_x = max(all_x)

    min_y = min(all_y)
    max_y = max(all_y)

    image_width = max_x - min_x
    image_height = max_y - min_y

    # Prevent divide-by-zero
    image_width = max(image_width, 1)
    image_height = max(image_height, 1)

    # -------------------------------------------------
    # SCALE FACTORS
    # -------------------------------------------------

    scale_x = machine_width / image_width
    scale_y = machine_height / image_height

    scale = min(scale_x, scale_y)

    # -------------------------------------------------
    # MAP TOOLPATH
    # -------------------------------------------------

    mapped_toolpath = []

    for segment in toolpath:

        mapped_segment = []

        for x, y in segment:

            mx = (x - min_x) * scale
            my = (y - min_y) * scale

            mapped_segment.append((mx, my))

        mapped_toolpath.append(mapped_segment)

    return mapped_toolpath