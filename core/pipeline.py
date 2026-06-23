from core.image_processor import load_and_detect_edges

from core.contour_utils import (
    extract_contours,
    clean_contour,
    reduce_contour
)

from core.contour_optimizer import optimize_contours

from core.toolpath import build_toolpath

from core.gcode_generator import generate_gcode

from core.gcode_export import save_gcode

from core.contour_order_optimizer import (
    optimize_contour_order
)
from core.contour_connector import (
    connect_contours
)
from core.machine_mapper import (
    map_to_machine_space
)


# =====================================================
# CENTRAL EXECUTION PIPELINE
# =====================================================

def run_pipeline(
    image_path,
    mode="balanced",
    risk_weight=1.0,
    save_output=True
):

    # =================================================
    # IMAGE PROCESSING
    # =================================================

    image, gray, edges = load_and_detect_edges(
        image_path
    )

    # =================================================
    # CONTOUR EXTRACTION
    # =================================================

    contours = extract_contours(edges)

    processed_contours = []

    for contour in contours:

        contour = clean_contour(contour)

        contour = reduce_contour(
            contour,
            max_points=80
        )

        processed_contours.append(contour)

    # =================================================
    # CONTOUR OPTIMIZATION
    # =================================================

    optimized_contours = optimize_contours(
        processed_contours,
        mode=mode,
        risk_weight=risk_weight
    )

    

    optimized_contours = optimize_contour_order(
    optimized_contours
)
    
    print("AFTER ORDERING:")
    for i,c in enumerate(optimized_contours):
      print("Contour", i,
          "Points:",
          len(c["points"]))
      
    final_points, final_path = connect_contours(
    optimized_contours
)
    
    print("CONNECTED POINTS:", len(final_points))
    print("CONNECTED PATH:", len(final_path))
    
    # =================================================
    # TOOLPATH GENERATION
    # =================================================

    toolpath = build_toolpath(
    optimized_contours
    )

    toolpath = map_to_machine_space(
       toolpath,
      machine_width=300,
      machine_height=300
)

    # =================================================
    # G-CODE GENERATION
    # =================================================

    gcode = generate_gcode(toolpath)

    # =================================================
    # OPTIONAL EXPORT
    # =================================================

    if save_output:

        save_gcode(
            gcode,
            filename="output.gcode"
        )

    # =================================================
    # RETURN PIPELINE DATA
    # =================================================

    return {

        "image": image,

        "gray": gray,

        "edges": edges,

        "contours": optimized_contours,

        "toolpath": toolpath,

        "gcode": gcode,

        "total_contours": len(
            optimized_contours
        ),

        "total_segments": len(
            toolpath
        ),

        "gcode_lines": len(
            gcode
        )
    }