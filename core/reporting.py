import json
import os
from datetime import datetime


# =====================================================
# SAVE EXPERIMENT
# =====================================================

def save_experiment(
    data,
    filename=None
):

    os.makedirs(
        "experiments",
        exist_ok=True
    )

    # -------------------------------------------------
    # AUTO NAME
    # -------------------------------------------------

    if filename is None:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"experiment_{timestamp}.json"
        )

    path = os.path.join(
        "experiments",
        filename
    )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    with open(path, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

    print(
        f"\nExperiment saved: {path}"
    )