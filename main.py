import random
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

risk_weight=1.0

# ==============IMPORTS=================
from core.learning import load_learning, save_learning
from core.predictor import predict_metrics
from core.logger import log_run
from core.patterns import generate_square
from utils.plotting import plot_points, plot_path
from core.qubo import build_qubo, compute_energy
from core.solver import advanced_solver
from core.path_generator import generate_random_paths, generate_row_wise_path
from core.evaluator import evaluate_paths
from core.metrics import (
    count_moves,
    estimate_time,
    count_turns,
    compute_risk,
    estimate_speed,
    compute_cost
)
from utils.plotting import compare_paths
from utils.visualization import plot_prediction_vs_actual, plot_learning_curve
from utils.comparison import plot_cost_comparison
from utils.metrics_display import display_metrics
from core.command_generator import path_to_commands
from core.serial_sender import send_commands

from core.image_processor import load_and_detect_edges

from core.contour_utils import (
    extract_contours,
    clean_contour,
    reduce_contour
)
from core.contour_optimizer import optimize_contours
from core.contour_connector import connect_contours
from core.toolpath import build_toolpath
import matplotlib.pyplot as plt
from core.gcode_generator import generate_gcode
from core.gcode_export import save_gcode
from core.convergence import hierarchical_convergence
from core.contour_order_optimizer import optimize_contour_order
from core.contour_direction_optimizer import optimize_contour_directions
from core.travel_optimizer import (
    compute_travel_metrics
)
from core.gcode_sender import send_gcode
from core.machine_limits import enforce_machine_limits
from core.machine_mapper import map_to_machine_space
from core.repeated_trials import run_trials
from core.validation import (
    run_trials,
    validate_runs
)

from utils.research_visualization import (
    plot_trial_statistics
)
from core.probabilistic_selector import probabilistic_selection
from core.diversity_filter import preserve_diversity

from core.reporting import (
    save_experiment
)
from aiml.model import (
    predict,
    risk_level,
    future_risk,
    recommendations
)


# =====================================================
# CONFIG
# =====================================================
MODE = "balanced"   # "speed" | "accuracy" | "balanced"

# =====================================================
# LOAD LEARNING (FIXED)
# =====================================================
learning_data = load_learning()
risk_weight = learning_data["risk_weight"]

print("\nLoaded Risk Weight:", risk_weight)

# =====================================================
# STEP 1 — IMAGE INPUT + POINT GENERATION
# =====================================================

print("\n========== STEP 1: IMAGE INPUT ==========")

image_path = "images/star.png"

image, gray, edges = load_and_detect_edges(image_path)

# Extract contour groups
contours = extract_contours(edges)

print("\nRAW CONTOURS:", len(contours))

for i, c in enumerate(contours):
    print(
        f"Contour {i+1}:",
        len(c),
        "points"
    )

# Process contours
processed_contours = []

for contour in contours:

    contour = clean_contour(contour)

    contour = reduce_contour(contour, max_points=80)

    processed_contours.append(contour)

print(
    "\nPROCESSED CONTOURS:",
    len(processed_contours)
)

for i, c in enumerate(processed_contours):
    print(
        f"Processed {i+1}:",
        len(c),
        "points"
    )

# =====================================================
# CONTOUR-WISE OPTIMIZATION
# =====================================================

print("\n========== CONTOUR OPTIMIZATION ==========")

optimized_contours = optimize_contours(
    processed_contours,
    mode=MODE,
    risk_weight=risk_weight
)

# =====================================================
# GLOBAL CONTOUR ORDER OPTIMIZATION
# =====================================================

optimized_contours = optimize_contour_order(
    optimized_contours
)

final_points, final_path = connect_contours(
    optimized_contours
)

# =====================================================
# CONTOUR DIRECTION OPTIMIZATION
# =====================================================

#optimized_contours = optimize_contour_directions(
   # optimized_contours
#)

print("Contour directions optimized.")



print("\nContour traversal optimized.")


print("Optimized contours:", len(optimized_contours))


# Merge all contours temporarily
points = final_points

print("Total contours:", len(processed_contours))
print("Total points:", len(points))

plot_points(points)

print("\nTotal Points Extracted:", len(points))

# =====================================================
# CONNECT CONTOURS
# =====================================================

#final_points, final_path = connect_contours(
 #   optimized_contours
#)

# =====================================================
# SINGLE CONTOUR PATH
# =====================================================



print(
    "\nFinal merged path size:",
    len(final_path)
)

print("\nFinal merged path size:", len(final_path))

# =====================================================
# BUILD TOOLPATH
# =====================================================

toolpath = build_toolpath(optimized_contours)

# =====================================================
# MACHINE SPACE MAPPING
# =====================================================

toolpath = map_to_machine_space(
    toolpath,
    machine_width=300,
    machine_height=300

)

toolpath = enforce_machine_limits(
    toolpath,
    max_x=300,
    max_y=300
)

print("\nToolpath mapped to machine space.")


# =====================================================
# TRAVEL ANALYSIS
# =====================================================

travel_data = compute_travel_metrics(
    toolpath
)

travel_distance = travel_data["travel_distance"]

travel_moves = travel_data["travel_moves"]

travel_time = travel_data["travel_time"]

print("\n========== TRAVEL ANALYSIS ==========")

print(
    "Travel Distance:",
    round(travel_distance, 2)
)

print(
    "Travel Moves:",
    travel_moves
)

print(
    "Estimated Travel Time:",
    round(travel_time, 4)
)

# =====================================================
# GENERATE G-CODE
# =====================================================

gcode = generate_gcode(toolpath)

print("\n========== GENERATED G-CODE ==========\n")

for line in gcode[:20]:
    print(line)

# Save file
save_gcode(gcode)

# =====================================================
# G-CODE EXECUTION SIMULATION
# =====================================================

print("\n========== G-CODE PREVIEW ==========\n")

for line in gcode[:30]:

    print(line)

# =====================================================
# SEND G-CODE TO ESP32
# =====================================================

# Uncomment later during hardware integration

# send_gcode(
#     gcode,
#     port="COM3"
# )

print("\nToolpath segments:", len(toolpath))

# =====================================================
# STEP 2 — QUBO MATRIX
# =====================================================
print("\n========== STEP 2: QUBO MATRIX ==========")

Q = build_qubo(points)
print("QUBO matrix shape:", Q.shape)

# =====================================================
# STEP 3 — SAMPLE RANDOM PATH
# =====================================================
print("\n========== STEP 3: SAMPLE RANDOM PATH ==========")

sample_path = list(range(len(points)))
random.shuffle(sample_path)

sample_energy = compute_energy(sample_path, Q)
print("Sample Energy:", sample_energy)

paths = generate_random_paths(len(points),num_paths=1)
random_path = paths[0]


# =====================================================
# STEP 4 — BASELINE (CLASSICAL)
# =====================================================
print("\n========== STEP 4: BASELINE ==========")

classical_path = generate_row_wise_path(points)
classical_energy = compute_energy(classical_path, Q)

print("Classical Energy:", classical_energy)

# =====================================================
# STEP 5 — MULTI PATH GENERATION
# =====================================================
print("\n========== STEP 5: MULTI-PATH GENERATION ==========")

paths = generate_random_paths(len(points), num_paths=50)
print("Total paths generated:", len(paths))

# =====================================================
# STEP 6 — EVALUATION
# =====================================================
print("\n========== STEP 6: ALL PATH ENERGIES ==========")

results = evaluate_paths(paths, Q)

# =====================================================
# PROBABILISTIC EXPLORATION
# =====================================================

results = probabilistic_selection(
    results,
    keep_count=25,
    temperature=5000
)

# =====================================================
# DIVERSITY PRESERVATION
# =====================================================

results = preserve_diversity(
    results,
    diversity_threshold=0.25
)

print(
    "\nDiversity preservation applied."
)

print(
    "Diverse candidates:",
    len(results)
)

print(
    "\nProbabilistic exploration applied."
)

print(
    "Remaining candidates:",
    len(results)
)

print("\n========== ALL PATH ENERGIES ==========")

for r in results:
    print(f"Path ID: {r['id']} → Energy: {round(r['energy'], 2)}")

# =====================================================
# STEP 7 — HIERARCHICAL CONVERGENCE
# =====================================================

final_candidates = hierarchical_convergence(results, points,Q)

print("\n--- FINAL CANDIDATES ---")

for r in final_candidates:

    print(
        f"ID: {r['id']} → Energy: {round(r['energy'], 2)}"
    )

# =====================================================
# STEP 8 — OPTIMIZATION
# =====================================================
print("\n========== STEP 8: OPTIMIZATION ==========")

optimized_results = []

for item in final_candidates:
    path = item["path"]

    opt_path, opt_cost = advanced_solver(
        points,
        Q,
        initial_path=path,
        iterations=20000,
        T=1500,
        mode=MODE,
        risk_weight=risk_weight
    )

    optimized_results.append({
        "path": opt_path,
        "cost": opt_cost
    })

# =====================================================
# STEP 9 — FINAL SELECTION
# =====================================================
print("\n========== STEP 9: FINAL SELECTION ==========")

optimized_sorted = sorted(optimized_results, key=lambda x: x["cost"])
final_best = optimized_sorted[0]

optimized_path = final_best["path"]
optimized_cost = final_best["cost"]

print(f"Mode: {MODE}")
print("Final Optimized Cost:", round(optimized_cost, 2))

# =====================================================
# EXPERIMENTAL VALIDATION
# =====================================================

# =====================================================
# STEP 9.5 — COMMAND GENERATION (NEW)
# =====================================================

from core.command_generator import path_to_commands

#optimized_commands = path_to_commands(points, optimized_path)

#print("\n========== GENERATED COMMANDS ==========")
#for cmd in optimized_commands:
 #   print(cmd)

# =====================================================
# STEP 9.6 — COMMAND SIMULATION (NEW)
# =====================================================

#print("\n========== SIMULATION ==========")

#for cmd in optimized_commands:
 #   print("Sending:", cmd)

# =====================================================
# STEP 9.7 — SERIAL SEND (NEW)
# =====================================================



# ⚠️ For now, comment this if ESP32 not connected
#send_commands(optimized_commands, port="COM3")


# =====================================================
# STEP 10 — METRICS + COMPARISON
# =====================================================
print("\n========== STEP 10: COMPARISON ==========")

# Classical
c_moves = count_moves(classical_path)
c_turns = count_turns(points, classical_path)
c_speed = estimate_speed(classical_energy)
c_risk = compute_risk(points, classical_path, c_speed)
c_time = estimate_time(classical_energy)
c_total_cost = compute_cost(points, classical_path, Q, MODE, risk_weight)

# Optimized
optimized_energy = compute_energy(optimized_path, Q)

o_moves = count_moves(optimized_path)
o_turns = count_turns(points, optimized_path)
o_speed = estimate_speed(optimized_energy)
o_risk = compute_risk(points, optimized_path, o_speed)
o_time = estimate_time(optimized_energy)
o_total_cost = compute_cost(points, optimized_path, Q, MODE, risk_weight)

# =====================================
# AIML INPUTS
# =====================================

distance_ai = optimized_energy

turns_ai = o_turns

# temporary vibration estimate
vibration_ai = round(o_risk, 2)

# =====================================
# AIML PREDICTION
# =====================================

probability = predict(
    distance_ai,
    turns_ai,
    vibration_ai
)

risk_ai = risk_level(
    probability
)

future_ai = future_risk(
    probability,
    vibration_ai
)

recommendation_ai = recommendations(
    probability,
    vibration_ai
)

print("\n========== AIML RESULT ==========\n")

print("Probability :", probability)

print("Risk Level  :", risk_ai)

print("Future Risk :", future_ai)

print("Recommendations:")

for item in recommendation_ai:
    print("-", item)

# =====================================================
# EXECUTION OVERHEAD COST
# =====================================================

execution_overhead = (
    travel_distance * 2
    + travel_moves * 50
)

o_total_cost += execution_overhead

classical_data = {
    "distance": classical_energy,
    "time": c_time,
    "risk": c_risk,
    "cost": c_total_cost
}

optimized_data = {
    "distance": optimized_energy,
    "time": o_time,
    "risk": o_risk,
    "cost": o_total_cost
}

display_metrics(classical_data, optimized_data)

# =====================================================
# EXPERIMENTAL VALIDATION
# =====================================================

trial_results = run_trials(

    points,
    Q,
    optimized_path,

    runs=5,

    mode=MODE,

    risk_weight=risk_weight
)

validation = validate_runs(
    trial_results
)

print(
    "\n========== VALIDATION =========="
)

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

# =====================================================
# RESEARCH VISUALIZATION
# =====================================================

plot_trial_statistics(
    trial_results
)


# =====================================================
# STEP 11 — PREDICTION
# =====================================================
prediction = predict_metrics(optimized_energy, o_turns, MODE)

print("\n--- PREDICTION ---")
print("Predicted Time:", prediction["time"])
print("Predicted Risk:", prediction["risk"])
print("Predicted Cost:", prediction["cost"])


# =====================================================
# STEP 12 — ERROR ANALYSIS
# =====================================================
error_time = abs(o_time - prediction["time"])
error_risk = abs(o_risk - prediction["risk"])
error_cost = abs(o_total_cost - prediction["cost"])

print("\n--- ERROR ANALYSIS ---")
print("Time Error:", round(error_time, 2))
print("Risk Error:", round(error_risk, 2))
print("Cost Error:", round(error_cost, 2))

# =====================================================
# STEP 12.2 — COST COMPARISON VISUALIZATION
# =====================================================

random_cost = compute_cost(points, random_path, Q, MODE, risk_weight)
predicted_cost = prediction["cost"]

plot_cost_comparison(random_cost, o_total_cost, predicted_cost)

# =====================================================
# STEP 12.5 — DIGITAL TWIN VISUALIZATION
# =====================================================

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

plot_prediction_vs_actual(predicted, actual)

# =====================================================
# STEP 13 — ERROR INTERPRETATION
# =====================================================
if o_risk > prediction["risk"]:
    print("⚠️ Risk underpredicted → system too optimistic")
elif o_risk < prediction["risk"]:
    print("⚠️ Risk overpredicted → system too conservative")
else:
    print("✅ Risk prediction is accurate")


# =====================================================
# SAVE EXPERIMENT
# =====================================================

save_experiment({

    "mode": MODE,

    "classical": classical_data,

    "optimized": optimized_data,

    "prediction": prediction,

    "risk_weight": risk_weight
})


# =====================================================
# STEP 14 — LEARNING UPDATE (YOUR BLOCK, FIXED)
# =====================================================
print("\n========== LEARNING UPDATE ==========")

learning_rate = 0.1

if o_risk > prediction["risk"]:
    risk_weight += learning_rate
elif o_risk < prediction["risk"]:
    risk_weight -= learning_rate

# ✅ ADD LIMITS (VERY IMPORTANT)
risk_weight = min(risk_weight, 3.0)   # upper cap
risk_weight = max(risk_weight, 0.1)   # lower cap

print("\n--- UPDATED PARAMETERS ---")
print("New Risk Weight:", round(risk_weight, 2))


# =====================================================
# SAVE LEARNING (VERY IMPORTANT)
# =====================================================
learning_data["risk_weight"] = risk_weight
save_learning(learning_data)


# =====================================================
# DISPLAY RESULTS (UNCHANGED)
# =====================================================
print("\nCLASSICAL:")
print("Distance:", round(classical_energy, 2))
print("Moves:", c_moves)
print("Turns:", c_turns)
print("Risk:", round(c_risk, 2))
print("Time:", round(c_time, 2))
print("Total Cost:", round(c_total_cost, 2))

print("\nOPTIMIZED:")
print("Distance:", round(optimized_energy, 2))
print("Moves:", o_moves)
print("Turns:", o_turns)
print("Risk:", round(o_risk, 2))
print("Time:", round(o_time, 2))
print("Total Cost:", round(o_total_cost, 2))


# =====================================================
# STEP 15 — LOGGING (UPGRADED)
# =====================================================
log_run({
    "mode": MODE,

    "distance": optimized_energy,
    "turns": o_turns,

    "predicted_time": prediction["time"],
    "predicted_risk": prediction["risk"],
    "predicted_cost": prediction["cost"],

    "actual_time": o_time,
    "actual_risk": o_risk,
    "actual_cost": o_total_cost,

    "error_time": error_time,
    "error_risk": error_risk,
    "error_cost": error_cost,

    "risk_weight": risk_weight
})

# =====================================================
# STEP 16 — IMPROVEMENT
# =====================================================
print("\n========== STEP 13: IMPROVEMENT ==========")

improvement = ((c_total_cost - o_total_cost) / c_total_cost) * 100
print("Cost Improvement:", round(improvement, 2), "%")

# =====================================================
# STEP 17 — VISUALIZATION
# =====================================================

plot_path(
    points,
    classical_path,
    "Classical (Row-wise)",
    filename="classical_path.png"
)

plot_path(
    points,
    optimized_path,
    "Optimized (Cost-based)",
    filename="optimized_path.png"
)

# =====================================================
# STEP 18 — COMPARISON VISUALIZATION (ADD THIS)
# =====================================================
compare_paths(points, classical_path, optimized_path)


# =====================================================
# STEP 19 — LEARNING CURVE VISUALIZATION
# =====================================================
plot_learning_curve("data/logs.json")

# =====================================================
# STEP 20 -- CONTOUR VISUALIZATION
# =====================================================

for i, contour_data in enumerate(optimized_contours):

    contour_points = contour_data["points"]
    contour_path = contour_data["path"]

    plot_path(
        contour_points,
        contour_path,
        f"Contour {i+1} Optimized"
    )

# =====================================================
#  STEP 21 - TOOLPATH VISUlization
# =====================================================

for i, segment in enumerate(toolpath):

    x = [p[0] for p in segment]
    y = [p[1] for p in segment]

    plt.figure()

    plt.plot(x, y, marker='o')

    plt.gca().invert_yaxis()

    plt.title(f"Toolpath Segment {i+1}")

    plt.grid()

    plt.savefig("graphs/graph_name.png")

    plt.show()

# =====================================================
# STEP 22 - API TEST
# =====================================================

from api import process_image

api_result = process_image(
    "images/star.png"
)

print(
    "\nAPI pipeline execution successful."
)

print(
    "Generated G-code lines:",
    len(api_result["gcode"])
)