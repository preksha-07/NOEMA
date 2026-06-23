from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from pydantic import BaseModel
from hardware_client import execute_plotter

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import shutil
import os

from core.execution_pipeline import execute_pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from datetime import datetime



app = FastAPI()


latest_execution = {

    "actual_time_seconds": 0,

    "actual_distance_mm": 0,

    "actual_vibration": 0
}




class PlotterRequest(BaseModel):

    commands: list[str]

class ExecutionResult(BaseModel):

    actual_time_seconds: float

    actual_distance_mm: float

    actual_vibration: int


app.mount(
    "/graphs",
    StaticFiles(directory="graphs"),
    name="graphs"
)

app.mount(
    "/static",
    StaticFiles(directory="."),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "message": "Optimization Backend Running"
    }


# =====================================================
# IMAGE UPLOAD + PROCESSING
# =====================================================

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    mode: str = Form("balanced")
):

    os.makedirs(
        "temp",
        exist_ok=True
    )

    save_path = f"temp/{file.filename}"

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    print(
    "MODE RECEIVED:",
    mode
)
    
    result = execute_pipeline(
        save_path, mode
    )

    print("\n===== FRONTEND REQUEST =====")

    print("Distance:", result["distance"])
    print("Turns:", result["turns"])
    print("Risk:", result["risk"])
    print("Cost:", result["cost"])

    print("============================\n")
    
    return {

    "message": "Image processed",

    "distance": result["distance"],

    "turns": result["turns"],

    "risk": result["risk"],

    "cost": result["cost"],

    "probability": result["probability"],

    "risk_level": result["risk_level"],

    "future_risk": result["future_risk"],

    "recommendations": result["recommendations"],

    "contours": result["contours"],
"segments": result["segments"],
"gcode_lines": result["gcode_lines"],
"classical_distance":
result["classical_distance"],

"classical_turns":
result["classical_turns"],

"classical_cost":
result["classical_cost"],

"predicted_time":
result["predicted_time"],

"predicted_risk":
result["predicted_risk"],

"predicted_cost":
result["predicted_cost"],

"time":
result["time"],

"error_time": result["error_time"],
"error_risk": result["error_risk"],
"error_cost": result["error_cost"],
"mode": mode,
"gcode":
result["gcode"],

"execution_state":
"READY_FOR_PLOTTER",

"hardware_vibration":
result.get("hardware_vibration",0)

}
# =====================================================
# OPTIMIZATION
# =====================================================

@app.get("/optimize")
def optimize():

    result = execute_pipeline(
        "images/star.png"
    )

    return {

        "toolpaths": result[
            "segments"
        ],

        "gcode_lines": result[
            "gcode_lines"
        ]

    }


# =====================================================
# METRICS
# =====================================================

@app.get("/metrics")
def metrics():

    result = execute_pipeline(
        "images/star.png"
    )

    return {
    "contours": result["contours"],
    "segments": result["segments"],
    "gcode_lines": result["gcode_lines"],
    "distance": result["distance"],
    "turns": result["turns"],
    "risk": result["risk"],
    "cost": result["cost"]
}

# =====================================================
# GCODE EXPORT
# =====================================================

@app.get("/gcode")
def gcode():

    result = execute_pipeline(
        "images/star.png"
    )

    return {

        "gcode": result[
            "gcode"
        ][:20]
    }

@app.get("/graphs-page")
def graphs_page():
    return FileResponse("graphs.html")




@app.post("/execute_plotter")
async def execute_plotter_route(
    request: PlotterRequest
):

    result = execute_plotter(
        request.commands
    )

    log_entry = {

        "timestamp":
        str(datetime.now()),

        "commands":
        len(request.commands),

        "status":
        "executed"
    }

    with open(
        "logs/plotter_runs.json",
        "r"
    ) as f:

        logs = json.load(f)

    logs.append(
        log_entry
    )

    with open(
        "logs/plotter_runs.json",
        "w"
    ) as f:

        json.dump(
            logs,
            f,
            indent=4
        )

    return result


@app.get("/plotter_status")
def plotter_status():

    return {
        "status":
        "connected"
    }

@app.get("/plotter_logs")
def plotter_logs():

    with open(
        "logs/plotter_runs.json",
        "r"
    ) as f:

        logs = json.load(f)

    return logs

@app.get("/system_status")
def system_status():

    return {

        "backend":
        "online",

        "aiml":
        "loaded",

        "plotter":
        "waiting_for_hardware"
    }

@app.post("/execution_results")
async def execution_results(
    data: ExecutionResult
):

    global latest_execution

    latest_execution = {

        "actual_time_seconds":
        data.actual_time_seconds,

        "actual_distance_mm":
        data.actual_distance_mm,

        "actual_vibration":
        data.actual_vibration
    }

    os.makedirs(
    "logs",
    exist_ok=True
)

    with open(
    "logs/latest_hardware.json",
    "w"
) as f:

        json.dump(
        latest_execution,
        f,
        indent=4
    )

    with open(
    "logs/latest_hardware.json",
    "w"
) as f:

        json.dump(
            latest_execution,
            f,
            indent=4
    )

    print("\n===== ACTUAL EXECUTION =====")

    print(
        "TIME:",
        data.actual_time_seconds
    )

    print(
        "DIST:",
        data.actual_distance_mm
    )

    print(
        "VIB:",
        data.actual_vibration
    )

    print("===========================\n")

    return {
        "status": "received"
    }

@app.get("/validation_logs")
def validation_logs():

    with open(
        "logs/validation_runs.json",
        "r"
    ) as f:

        logs = json.load(f)

    return logs

@app.get("/latest_execution")
def latest_execution_metrics():

    return latest_execution
