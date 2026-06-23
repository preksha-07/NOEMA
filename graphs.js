// ==========================================
// KPI COUNT-UP ANIMATION
// ==========================================

const data =
JSON.parse(
    localStorage.getItem(
        "noema_results"
    )
);

if(data){

    const geometry =
    document.getElementById(
        "geometryType"
    );

    if(geometry){

        geometry.innerText =
        "Custom Upload";
    }

    const candidates =
    document.getElementById(
        "candidateTotal"
    );

    if(candidates){

        candidates.innerText =
        "1000";
    }

    const selected =
    document.getElementById(
        "selectedPath"
    );

    if(selected){

        selected.innerText =
        "Quantum Optimized Path";
    }
}

fetch(
    "http://172.17.10.122:8000/latest_execution"
)
.then(r => r.json())
.then(data => {

    document.getElementById(
        "vibrationValue"
    ).innerText =
    data.actual_vibration;

});

// ==========================================
// CHART COMMON SETTINGS
// ==========================================



// ==========================================
// ENERGY DISTRIBUTION
// ==========================================


// ==========================================
// COST
// ==========================================



// ==========================================
// DISTANCE
// ==========================================


// ==========================================
// RISK
// ==========================================



// ==========================================
// TURNS
// ==========================================



// ==========================================
// DIGITAL TWIN
// ==========================================



// ==========================================
// LEARNING SYSTEM
// ==========================================



// ==========================================
// ML ACCURACY
// ==========================================



// ==========================================
// ML CONFIDENCE
// ==========================================



document.addEventListener(
    "DOMContentLoaded",
    () => {

        const timestamp =
            new Date().getTime();

        const graphMap = {
            
            classical:
            "http://172.17.10.122:8000/graphs/classical_path.png",

            optimized:
            "http://172.17.10.122:8000/graphs/optimized_path.png",

            comparison:
            "http://172.17.10.122:8000/graphs/path_comparison.png",

            digitalTwin:
            "http://172.17.10.122:8000/graphs/digital_twin.png",

            learning:
            "http://172.17.10.122:8000/graphs/learning_curve.png",

            cost:
            "http://172.17.10.122:8000/graphs/cost_stability.png",

            risk:
            "http://172.17.10.122:8000/graphs/risk_stability.png",

            distance:
            "http://172.17.10.122:8000/graphs/distance_stability.png",

            turns:
            "http://172.17.10.122:8000/graphs/turn_stability.png",

            
        };

        Object.entries(graphMap).forEach(
            ([id, url]) => {

                const img =
                    document.getElementById(id);

                if (img) {

                    img.src =
                        url +
                        "?t=" +
                        timestamp;
                }
            }
        );
    }
);


