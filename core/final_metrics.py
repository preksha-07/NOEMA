def build_metrics(
    distance,
    turns,
    risk,
    cost,
    improvement
):

    return {

        "distance": round(distance, 2),

        "turns": turns,

        "risk": round(risk, 2),

        "cost": round(cost, 2),

        "improvement": round(
            improvement,
            2
        )
    }