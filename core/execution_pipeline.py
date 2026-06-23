from core.image_processor import load_and_detect_edges
import numpy as np
from core.contour_utils import (
    extract_contours,
    clean_contour,
    reduce_contour
)
import os 
import json
from core.contour_optimizer import (
    optimize_contours
)

from core.contour_order_optimizer import (
    optimize_contour_order
)

from core.contour_connector import (
    connect_contours
)

from core.qubo import (
    build_qubo,
    compute_energy
)

from core.path_generator import (
    generate_random_paths,
    generate_row_wise_path
)

from core.evaluator import (
    evaluate_paths
)

from core.probabilistic_selector import (
    probabilistic_selection
)

from core.diversity_filter import (
    preserve_diversity
)

from core.convergence import (
    hierarchical_convergence
)

from core.solver import (
    advanced_solver
)
from core.metrics import (
    count_moves,
    count_turns,
    estimate_speed,
    estimate_time,
    compute_risk
)

from core.metrics import (
    compute_cost
)
from aiml.model import (
    predict,
    risk_level,
    future_risk,
    recommendations
)
from core.gcode_generator import generate_gcode

from core.toolpath import build_toolpath
from core.logger import log_run
from core.validation import (
    run_trials,
    validate_runs
)
from core.predictor import predict_metrics
from core.learning import (
    load_learning,
    save_learning
)
from utils.visualization import (
    plot_prediction_vs_actual,
    plot_learning_curve
)
from utils.visualization import (
    plot_prediction_vs_actual,
    plot_learning_curve,
    plot_cost_stability
)
from utils.visualization import (
    plot_prediction_vs_actual,
    plot_learning_curve,
    plot_cost_stability,
    plot_risk_stability,
    plot_distance_stability,
    plot_turn_stability
)
from utils.plotting import (
    plot_path,
    compare_paths
)
from core.metrics import pixels_to_mm




def execute_pipeline(
    image_path,
    mode="balanced",
    risk_weight=1.0
):
    hardware_vibration = 0

    if os.path.exists(
        "logs/latest_hardware.json"
    ):

        with open(
            "logs/latest_hardware.json",
            "r"
        ) as f:

            hw = json.load(f)

        hardware_vibration = (
            hw.get(
                "actual_vibration",
                0
            )
            /
            10000
        )
    
    # ============================================
    # IMAGE PROCESSING
    # ============================================

    image, gray, edges = load_and_detect_edges(
        image_path
    )

    contours = extract_contours(edges)

    # =====================================
    # SAFETY LIMIT
    # =====================================

    MAX_CONTOURS = 10

    if len(contours) > MAX_CONTOURS:

        print(
        f"Too many contours detected: {len(contours)}"
    )

        contours = sorted(
    contours,
    key=lambda c: len(c),
    reverse=True
)

        contours = contours[:10]

        print(
        f"Using first {MAX_CONTOURS} contours"
    )

    processed_contours = []

    for contour in contours:

        contour = clean_contour(contour)

        contour = reduce_contour(
            contour,
            max_points=60
        )

        processed_contours.append(contour)

    # ============================================
    # CONTOUR OPTIMIZATION
    # ============================================

    optimized_contours = optimize_contours(
        processed_contours,
        mode=mode,
        risk_weight=risk_weight
    )

    optimized_contours = optimize_contour_order(
        optimized_contours
    )

    final_points, final_path = connect_contours(
        optimized_contours
    )

    print(
    "TOTAL FINAL POINTS:",
    len(final_points)
)

    MAX_POINTS = 500

    if len(final_points) > MAX_POINTS:

        print(
        f"Reducing points from {len(final_points)} to {MAX_POINTS}"
    )

        indices = np.linspace(
    0,
    len(final_points) - 1,
    MAX_POINTS,
    dtype=int
)

        final_points = [
    final_points[i]
    for i in indices
]

    # ============================================
    # QUBO
    # ============================================
    print(
    "QUBO POINT COUNT:",
    len(final_points)
)
    
    Q = build_qubo(final_points)

    # ============================================
    # BASELINE
    # ============================================

    classical_path = generate_row_wise_path(
        final_points
    )

    # =====================================
    # CLASSICAL METRICS
    # =====================================

    classical_distance = compute_energy(
    classical_path,
    Q
)

    classical_turns = count_turns(
    final_points,
    classical_path
)

    classical_speed = estimate_speed(
    classical_distance
)

    classical_risk = compute_risk(
    final_points,
    classical_path,
    classical_speed,
    hardware_vibration
)

    classical_cost = compute_cost(
    final_points,
    classical_path,
    Q,
    mode,
    risk_weight
)

    # ============================================
    # PATH GENERATION
    # ============================================

    paths = generate_random_paths(
        len(final_points),
        num_paths=500
    )

    # ============================================
    # EVALUATION
    # ============================================

    results = evaluate_paths(
        paths,
        Q
    )

    # ============================================
    # PROBABILISTIC FILTER
    # ============================================

    results = probabilistic_selection(
        results,
        keep_count=25,
        temperature=5000
    )

    # ============================================
    # DIVERSITY FILTER
    # ============================================

    results = preserve_diversity(
        results,
        diversity_threshold=0.25
    )

    # ============================================
    # CONVERGENCE
    # ============================================

    final_candidates = hierarchical_convergence(
        results,
        final_points,
        Q
    )

    # ============================================
    # ADVANCED SOLVER
    # ============================================

    optimized_results = []

    for item in final_candidates:

        path = item["path"]

        opt_path, opt_cost = advanced_solver(
            final_points,
            Q,
            initial_path=path,
            iterations=20000,
            T=1500,
            mode=mode,
            risk_weight=risk_weight
        )

        optimized_results.append({

            "path": opt_path,

            "cost": opt_cost
        })

    # ============================================
    # FINAL SELECTION
    # ============================================

    optimized_sorted = sorted(
        optimized_results,
        key=lambda x: x["cost"]
    )

    final_best = optimized_sorted[0]

    optimized_path = final_best["path"]

    optimized_cost = final_best["cost"]

    optimized_energy = compute_energy(
    optimized_path,
    Q
)

    o_moves = count_moves(
    optimized_path
)

    o_turns = count_turns(
    final_points,
    optimized_path
)

    base_speed = 1.0

    if mode == "speed":
        base_speed = 1.5

    elif mode == "accuracy":
        base_speed = 0.7

    o_speed = estimate_speed(
    optimized_energy,
    base_speed
)

    o_risk = compute_risk(
    final_points,
    optimized_path,
    o_speed,
    hardware_vibration
)

    o_time = estimate_time(
    optimized_energy
)

    o_total_cost = compute_cost(
    final_points,
    optimized_path,
    Q,
    mode,
    risk_weight
)
    # =====================================
    # PREDICTION
    # =====================================

    prediction = predict_metrics(
    pixels_to_mm(
        optimized_energy
    ),
    o_turns,
    mode
)
    
    prediction["time"] = round(
    prediction["time"],
    2
)

    prediction["risk"] = round(
    prediction["risk"],
    2
)

    prediction["cost"] = round(
    prediction["cost"],
    2
)

    print("\n--- PREDICTION ---")

    print(
    "Predicted Time:",
    prediction["time"]
)

    print(
    "Predicted Risk:",
    prediction["risk"]
)

    print(
    "Predicted Cost:",
    prediction["cost"]
)
    
    # =====================================
    # ERROR ANALYSIS
    # =====================================

    error_time = abs(
    o_time - prediction["time"]
)

    error_risk = abs(
    o_risk - prediction["risk"]
)

    error_cost = abs(
    o_total_cost - prediction["cost"]
)

    print("\n--- ERROR ANALYSIS ---")

    print(
    "Time Error:",
    round(error_time, 2)
)

    print(
    "Risk Error:",
    round(error_risk, 2)
)

    print(
    "Cost Error:",
    round(error_cost, 2)
)
    
    # =====================================
    # LEARNING UPDATE
    # =====================================

    learning_data = load_learning()

    hardware_vibration = 0

    if os.path.exists(
    "logs/latest_hardware.json"
):

        with open(
            "logs/latest_hardware.json",
             "r"
    ) as f:

            hw = json.load(f)

        hardware_vibration = hw.get(
        "actual_vibration",
        0
    )

        hardware_vibration = (
    hardware_vibration / 10000
)

    learning_rate = 0.1

    if hardware_vibration > 0:

        if hardware_vibration > 2.0:

             risk_weight += 0.2

        elif hardware_vibration < 1.0:

            risk_weight -= 0.1

    else:

        if o_risk > prediction["risk"]:

            risk_weight += learning_rate

        elif o_risk < prediction["risk"]:

            risk_weight -= learning_rate

    risk_weight = min(
    risk_weight,
    3.0
)

    risk_weight = max(
    risk_weight,
    0.1
)

    learning_data["risk_weight"] = risk_weight

    save_learning(
    learning_data
)

    print("\n========== LEARNING UPDATE ==========")

    print(
    "New Risk Weight:",
    risk_weight
)
    
    predicted = {

    "time": prediction["time"],

    "risk": prediction["risk"],

    "cost": prediction["cost"]
}

    actual = {

    "time": o_time,

    "risk": o_risk,

    "cost": o_total_cost
}

    plot_prediction_vs_actual(
    predicted,
    actual
)
    plot_learning_curve(
    "logs/logs.json"
)
    

    # =====================================
    # VALIDATION
    # =====================================

    trial_results = run_trials(

    final_points,
    Q,
    optimized_path,

    runs=5,

    mode=mode,

    risk_weight=risk_weight
)

    validation = validate_runs(
    trial_results
)

    
    print("\n========== VALIDATION ==========")

    print(
    "Average Cost:",
    round(validation["cost_mean"], 2)
)

    print(
    "Cost Std Dev:",
    round(validation["cost_std"], 2)
)

    print(
    "Average Risk:",
    round(validation["risk_mean"], 2)
)

    print(
    "Risk Std Dev:",
    round(validation["risk_std"], 2)
)

    print(
    "Average Distance:",
    round(validation["distance_mean"], 2)
)

    print(
    "Distance Std Dev:",
    round(validation["distance_std"], 2)
)

    print(
    "Average Turns:",
    round(validation["turn_mean"], 2)
)

    print(
    "Turn Std Dev:",
    round(validation["turn_std"], 2)
)
    
    plot_cost_stability(
    trial_results
)
    plot_risk_stability(
    trial_results
)

    plot_distance_stability(
    trial_results
)

    plot_turn_stability(
    trial_results
)
    
    plot_path(
    final_points,
    classical_path,
    "Classical (Row-wise)",
    filename="classical_path.png"
)

    plot_path(
    final_points,
    optimized_path,
    "Optimized (Cost-based)",
    filename="optimized_path.png"
)

    compare_paths(
    final_points,
    classical_path,
    optimized_path
)

    print("\nAIML INPUTS")
    print(
    "Distance:",
    pixels_to_mm(
        optimized_energy
    )
)
    print("Turns:", o_turns)
    
    print("Vibration:", o_risk)

    vibration_ai = (
    hardware_vibration
    if hardware_vibration > 0
    else o_risk
)

    probability = predict(
    pixels_to_mm(
        optimized_energy
    ),
    o_turns,
    vibration_ai
)
    
    print(
    "FINAL PROBABILITY:",
    probability
)

    risk_ai = risk_level(probability)

    future_ai = future_risk(
    probability,
    vibration_ai
)

    recommendation_ai = recommendations(
    probability,
    vibration_ai
)

    toolpath = build_toolpath(
    optimized_contours
)

    gcode = generate_gcode(toolpath)

    log_run({

    "distance": round(
    pixels_to_mm(
        optimized_energy
    ),
    2
),

    "turns": o_turns,

    "risk": round(
        o_risk,
        2
    ),

    "cost": round(
        o_total_cost,
        2
    ),

    "probability": probability,

    "risk_level": risk_ai,

    "future_risk": future_ai,
    "predicted_time":
    prediction["time"],

    "predicted_risk":
    prediction["risk"],

    "predicted_cost":
    prediction["cost"],

    "actual_time":
    o_time,

    "actual_risk":
    o_risk,

    "actual_cost":
    o_total_cost,

    "error_time":
    error_time,

    "error_risk":
    error_risk,

    "error_cost":
    error_cost,

    
    "risk_weight":
    risk_weight,

    
"gcode": gcode,

"hardware_vibration":
hardware_vibration,
})

    

    # ============================================
    # RETURN
    # ============================================

    return {

        "image": image,

        "gray": gray,

        "edges": edges,

        "processed_contours": processed_contours,

        "optimized_contours": optimized_contours,

        "final_points": final_points,

        "final_path": final_path,

        "Q": Q,

        "classical_path": classical_path,

        "candidate_results": results,

        "filtered_results": results,

        "final_candidates": final_candidates,

        "optimized_path": optimized_path,

        "optimized_cost": optimized_cost,
        "validation": validation,
       "distance": round(
    pixels_to_mm(
        optimized_energy
    ),
    2
),

"moves": o_moves,

"turns": o_turns,

"risk": round(
    o_risk,
    2
),

"time": round(
    o_time,
    2
),

"cost": round(
    o_total_cost,
    2
),

"probability": probability,
"risk_level": risk_ai,
"future_risk": future_ai,
"recommendations": recommendation_ai,
"contours": len(optimized_contours),
"segments": len(optimized_contours),
"gcode_lines": len(gcode),
"gcode": gcode,
"predicted_time":
    prediction["time"],

"predicted_risk":
    prediction["risk"],

"predicted_cost":
    prediction["cost"],

"error_time":
round(error_time, 2),

"error_risk":
round(error_risk, 2),

"error_cost":
round(error_cost, 2),

    "classical_distance":
round(
    pixels_to_mm(
        classical_distance
    ),
    2
),

"classical_turns":
classical_turns,

"classical_cost":
round(classical_cost, 2),




    }