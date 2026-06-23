# =====================================================
# MULTI-STAGE MANUFACTURING CONVERGENCE
# =====================================================

from core.metrics import (
    count_turns,
    estimate_speed,
    compute_risk
)

from core.qubo import compute_energy


# =====================================================
# STAGE FILTER
# =====================================================

def filter_stage(
    candidates,
    keep_count,
    key
):

    sorted_candidates = sorted(
        candidates,
        key=key
    )

    return sorted_candidates[:keep_count]


# =====================================================
# HIERARCHICAL CONVERGENCE
# =====================================================

def hierarchical_convergence(
    results,
    points,
    Q
):

    print("\n========== CONVERGENCE ENGINE ==========")

    # =================================================
    # STAGE 1 — DISTANCE FILTER
    # 1000 → 200
    # =================================================

    stage_1 = filter_stage(
        results,
        keep_count=min(200, len(results)),
        key=lambda x: x["energy"]
    )

    print(
        f"Stage 1 (Distance): "
        f"{len(results)} → {len(stage_1)}"
    )

    # =================================================
    # STAGE 2 — TURN FILTER
    # 200 → 50
    # =================================================

    for item in stage_1:

        path = item["path"]

        item["turns"] = count_turns(
            points,
            path
        )

    stage_2 = filter_stage(
        stage_1,
        keep_count=min(50, len(stage_1)),
        key=lambda x: x["turns"]
    )

    print(
        f"Stage 2 (Turns): "
        f"{len(stage_1)} → {len(stage_2)}"
    )

    # =================================================
    # STAGE 3 — RISK FILTER
    # 50 → 10
    # =================================================

    for item in stage_2:

        path = item["path"]

        distance = compute_energy(path, Q)

        speed = estimate_speed(distance)

        item["risk"] = compute_risk(
            points,
            path,
            speed
        )

    stage_3 = filter_stage(
        stage_2,
        keep_count=min(10, len(stage_2)),
        key=lambda x: x["risk"]
    )

    print(
        f"Stage 3 (Risk): "
        f"{len(stage_2)} → {len(stage_3)}"
    )

    # =================================================
    # FINAL STAGE — COMBINED SCORE
    # 10 → 3
    # =================================================

    for item in stage_3:

        item["combined_score"] = (
            item["energy"]
            + item["risk"] * 10
            + item["turns"] * 5
        )

    final_stage = filter_stage(
        stage_3,
        keep_count=min(3, len(stage_3)),
        key=lambda x: x["combined_score"]
    )

    print(
        f"Final Stage: "
        f"{len(stage_3)} → {len(final_stage)}"
    )

    return final_stage