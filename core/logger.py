import json
import os
from datetime import datetime


# =====================================================
# LOG DIRECTORY
# =====================================================

LOG_DIR = "logs"

LOG_FILE = os.path.join(
    LOG_DIR,
    "logs.json"
)


# =====================================================
# INITIALIZE LOG SYSTEM
# =====================================================

def init_log():

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w") as f:

            json.dump([], f)


# =====================================================
# SAVE LOG ENTRY
# =====================================================

def log_run(data):

    init_log()

    with open(LOG_FILE, "r") as f:

        logs = json.load(f)

    # -------------------------------------------------
    # TIMESTAMP
    # -------------------------------------------------

    data["timestamp"] = str(
        datetime.now()
    )

    logs.append(data)

    with open(LOG_FILE, "w") as f:

        json.dump(
            logs,
            f,
            indent=4
        )

    print(
        "\nLog saved successfully."
    )