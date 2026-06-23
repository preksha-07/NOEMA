// ============================================
// MODE SELECTOR
// ============================================

let selectedMode =
"balanced";

const modeButtons =
document.querySelectorAll(
    ".mode-buttons button"
);

modeButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            modeButtons.forEach(
                btn =>
                btn.classList.remove(
                    "active-mode"
                )
            );

            button.classList.add(
                "active-mode"
            );

            selectedMode =
            button.innerText
            .trim()
            .toLowerCase();

            document.getElementById(
    "modeStatus"
).innerText =

button.innerText
.trim()
+
" Mode";

            console.log(
                "MODE:",
                selectedMode
            );

        }
    );

});

// ============================================
// FILE UPLOAD
// ============================================

const fileInput =
document.querySelector(
    'input[type="file"]'
);

if(fileInput){

    fileInput.addEventListener(
        "change",
        function(){

            if(
                this.files.length > 0
            ){

                alert(
                    "Loaded: " +
                    this.files[0].name
                );

            }

        }
    );

}





// ============================================
// METRIC ANIMATION
// ============================================

const metricValues =
document.querySelectorAll(
    ".metric-card p"
);

setInterval(()=>{

    metricValues.forEach(
        metric => {

            metric.style.transform =
            "scale(1.05)";

            setTimeout(()=>{

                metric.style.transform =
                "scale(1)";

            },300);

        }
    );

},3000);

// ============================================
// ACTION BUTTONS
// ============================================

const actionButtons =
document.querySelectorAll(
    ".action-btn"
);

actionButtons.forEach(btn => {

    btn.addEventListener(
        "click",
        () => {

            btn.innerText =
            "Completed ✓";

            setTimeout(()=>{

                btn.innerText =
                btn.getAttribute(
                    "data-original"
                ) ||
                btn.innerText;

            },2000);

        }
    );

});

// save original text

actionButtons.forEach(btn => {

    btn.setAttribute(
        "data-original",
        btn.innerText
    );

});

// ============================================
// SCROLL TO TOP
// ============================================

function scrollToTop(){

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}

// ============================================
//  ESP32
// ============================================


const plotterBtn =
document.getElementById(
    "executePlotterBtn"
);

if(plotterBtn){

    plotterBtn.addEventListener(
        "click",
        executePlotter
    );

}

async function executePlotter()
{
    const gcode =
        JSON.parse(
            localStorage.getItem(
                "latest_gcode"
            )
        );

    if (!gcode)
    {
        alert(
            "Run optimization first"
        );
        return;
    }

    try
    {
        const response =
            await fetch(
                "http://172.17.10.122:8000/execute_plotter",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        commands: gcode
                    })
                }
            );

        const text =
        await response.text();

        console.log(text);

        try {

        const result =
        JSON.parse(text);

        console.log(result);

        }
        catch(e){

        alert(text);

        }

        if(result.actual_time_seconds)
{
    document.getElementById(
        "actualTime"
    ).innerText =
    result.actual_time_seconds;
}

        const actualDistance =
document.getElementById(
    "actualDistance"
);

    if(
    actualDistance &&
    result.actual_distance_mm
){
    actualDistance.innerText =
    result.actual_distance_mm;
}

        if(result.actual_vibration)
{
    document.getElementById(
        "actualVibration"
    ).innerText =
    result.actual_vibration;
}

        alert(
            result.status ||
            "Request sent"
        );
    }

    catch(error)
{
    console.error(error);

    alert(
        error.message
    );
}

}
// ============================================
// BACKEND INTEGRATION
// ============================================



const optimizeBtn =
document.getElementById(
    "optimizeBtn"
);

if(optimizeBtn){

    optimizeBtn.addEventListener(
        "click",
        async () => {

            const file =
            document.getElementById(
                "imageUpload"
            ).files[0];

            if(!file){

                alert(
                    "Please upload an image first."
                );

                return;
            }

            const formData =
            new FormData();

            formData.append(
                "file",
                file
            );

            formData.append(
    "mode",
    selectedMode
);

            try{

                const response =
                await fetch(
                    "http://172.17.10.122:8000/upload-image",
                    {
                        method:"POST",
                        body:formData
                    }
                );

                const data =
                await response.json();

                

                document.getElementById(
    "currentMode"
).innerText =
data.mode.charAt(0).toUpperCase()
+
data.mode.slice(1);

                localStorage.setItem(
    "noema_results",
    JSON.stringify(data)
);

localStorage.setItem(
    "latest_gcode",
    JSON.stringify(
        data.gcode
    )
);

console.log(
    "SAVED:",
    localStorage.getItem(
        "noema_results"
    )
);

                const predictionError =

(
    data.error_cost
    /
    data.cost
)
*
100;

document.getElementById(
    "predictionError"
).innerText =
predictionError.toFixed(1) + "%";

                

                document.getElementById(
    "optimizedDistance"
).innerText =
data.distance.toFixed(2);

document.getElementById(
    "optimizedTurns"
).innerText =
data.turns;

document.getElementById(
    "optimizedCost"
).innerText =
data.cost.toFixed(2);

document.getElementById(
    "classicalDistance"
).innerText =
data.classical_distance.toFixed(2);

document.getElementById(
    "classicalTurns"
).innerText =
data.classical_turns;

document.getElementById(
    "classicalCost"
).innerText =
data.classical_cost.toFixed(2);

document.getElementById(
    "predictedTime"
).innerText =
data.predicted_time
? data.predicted_time.toFixed(2)
: "--";

document.getElementById(
    "predictedRisk"
).innerText =
data.predicted_risk
? data.predicted_risk.toFixed(2)
: "--";

document.getElementById(
    "predictedCost"
).innerText =
data.predicted_cost
? data.predicted_cost.toFixed(2)
: "--";


document.getElementById(
    "actualTime"
).innerText =
data.time.toFixed(2);

document.getElementById(
    "actualRisk"
).innerText =
data.risk.toFixed(2);

if(
    data.actual_vibration
){
    document.getElementById(
        "actualVibration"
    ).innerText =
    data.actual_vibration;
}

document.getElementById(
    "actualCost"
).innerText =
data.cost.toFixed(2);


const timeError =
document.getElementById(
    "timeError"
);

if(timeError){

    timeError.innerText =
    "Time: " +
    data.error_time;
}

const riskError =
document.getElementById(
    "riskError"
);

if(riskError){

    riskError.innerText =
    "Risk: " +
    data.error_risk;
}

const costError =
document.getElementById(
    "costError"
);

if(costError){

    costError.innerText =
    "Cost: " +
    data.error_cost;
}

const improvement =

(
    (
        data.classical_cost
        -
        data.cost
    )
    /
    data.classical_cost
)
*
100;

document.getElementById(
    "improvementPercent"
).innerText =
improvement.toFixed(1) + "%";

                console.log(data);

                const timestamp =
Date.now();

const terminal =
document.getElementById(
    "terminal-output"
);

if(
    terminal &&
    data.gcode
){

    terminal.innerHTML =
    "> NOEMA TERMINAL READY\n\n";

    data.gcode.forEach(
        line => {

            terminal.innerHTML +=
            line +
            "<br>";

        }
    );

    terminal.innerHTML +=
    "<br><br>PROGRAM COMPLETE";
}


const classicalImg =
document.getElementById(
    "classicalImage"
);

const optimizedImg =
document.getElementById(
    "optimizedImage"
);

if(classicalImg){

    classicalImg.src =
    "http://172.17.10.122:8000/graphs/classical_path.png?t="
    + timestamp;
}

if(optimizedImg){

    optimizedImg.src =
    "http://172.17.10.122:8000/graphs/optimized_path.png?t="
    + timestamp;
}
                
                document.getElementById(
    "riskValue"
).innerText = data.risk;

document.getElementById(
    "timeValue"
).innerText =
data.time.toFixed(2);

document.getElementById(
    "turnValue"
).innerText = data.turns;

document.getElementById(
    "apiResults"
).innerHTML = `

<h3>Optimization Results</h3>

<p>Contours: ${data.contours}</p>

<p>Segments: ${data.segments}</p>

<p>G-Code Lines: ${data.gcode_lines}</p>

<p>Distance: ${data.distance}</p>

<p>Turns: ${data.turns}</p>

<p>Risk: ${data.risk}</p>

<p>Cost: ${data.cost}</p>

<hr>

<h3>AI Analysis</h3>

<p>Probability: ${data.probability}</p>

<p>Risk Level: ${data.risk_level}</p>

<p>Future Risk: ${data.future_risk}</p>

<p>Recommendations:</p>

<ul>
${data.recommendations.map(
    r => `<li>${r}</li>`
).join("")}
</ul>

`;

            }

            catch(error){

                console.error(error);

                alert(
                    "Backend connection failed."
                );

            }

        }
    );

}

function resetWorkspace(){

    localStorage.removeItem(
        "noema_results"
    );

    location.reload();
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const savedData =
        JSON.parse(
            localStorage.getItem(
                "noema_results"
            )
        );

        if(!savedData)
            return;

        document.getElementById(
            "optimizedDistance"
        ).innerText =
        savedData.distance.toFixed(2);

        document.getElementById(
            "optimizedTurns"
        ).innerText =
        savedData.turns;

        document.getElementById(
            "optimizedCost"
        ).innerText =
        savedData.cost.toFixed(2);

        document.getElementById(
            "classicalDistance"
        ).innerText =
        savedData.classical_distance.toFixed(2);

        document.getElementById(
            "classicalTurns"
        ).innerText =
        savedData.classical_turns;

        document.getElementById(
            "classicalCost"
        ).innerText =
        savedData.classical_cost.toFixed(2);

        document.getElementById(
            "riskValue"
        ).innerText =
        savedData.risk;

        document.getElementById(
            "timeValue"
        ).innerText =
        savedData.time.toFixed(2);

        document.getElementById(
            "turnValue"
        ).innerText =
        savedData.turns;
    }
);

function resetWorkspace(){

    localStorage.removeItem(
        "noema_results"
    );

    window.scrollTo(
        0,
        0
    );

    location.reload();
}