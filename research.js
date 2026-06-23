/* =========================================
   SCROLL REVEAL
========================================= */

const observer = new IntersectionObserver(

(entries) => {

entries.forEach(entry => {

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

},

{
threshold:0.15
}

);

document
.querySelectorAll(
".glass-card, .pipeline-card, .metric-card, .section-title"
)
.forEach(el => observer.observe(el));



/* =========================================
   CONVERGENCE PULSE
========================================= */

const stages =
document.querySelectorAll(
".convergence-stage"
);

let active = 0;

function animateConvergence(){

stages.forEach(
s => s.classList.remove("active-stage")
);

stages[active]
.classList.add("active-stage");

active++;

if(active >= stages.length){

active = 0;

}

}

setInterval(
animateConvergence,
1000
);



/* =========================================
   METRIC COUNTERS
========================================= */

function animateValue(
element,
start,
end,
duration
){

let startTime = null;

function update(currentTime){

if(!startTime)
startTime = currentTime;

const progress =
Math.min(
(currentTime - startTime)
/ duration,
1
);

const value =
start +
(end - start) * progress;

element.innerText =
Math.floor(value) + "%";

if(progress < 1){

requestAnimationFrame(update);

}

}

requestAnimationFrame(update);

}

const metricCards =
document.querySelectorAll(
".metric-value"
);

const metricTargets =
[
95,
80,
60,
90
];

metricCards.forEach(
(card,index) => {

const observer =
new IntersectionObserver(

(entries)=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

animateValue(
card,
0,
metricTargets[index],
2000
);

observer.disconnect();

}

});

}

);

observer.observe(card);

}

);



/* =========================================
   PIPELINE ANIMATION
========================================= */

const pipelineNodes =
document.querySelectorAll(
".pipeline-node"
);

let pipelineIndex = 0;

function animatePipeline(){

pipelineNodes.forEach(
node =>
node.classList.remove(
"pipeline-active"
)
);

pipelineNodes[pipelineIndex]
.classList.add(
"pipeline-active"
);

pipelineIndex++;

if(
pipelineIndex >=
pipelineNodes.length
){

pipelineIndex = 0;

}

}

setInterval(
animatePipeline,
900
);



/* =========================================
   DIGITAL TWIN
========================================= */

const twinCards =
document.querySelectorAll(
".comparison-panel .glass-card"
);

function twinPulse(){

twinCards.forEach(
card => {

card.classList.add(
"twin-active"
);

setTimeout(()=>{

card.classList.remove(
"twin-active"
);

},600);

}

);

}

setInterval(
twinPulse,
2500
);



/* =========================================
   TERMINAL SCROLL
========================================= */

const terminal =
document.querySelector(
".terminal-window"
);

if(terminal){

setInterval(()=>{

terminal.scrollTop =
terminal.scrollHeight;

},1000);

}



/* =========================================
   HERO TAG FLOAT
========================================= */

const tags =
document.querySelectorAll(
".hero-tags span"
);

tags.forEach(
(tag,index)=>{

tag.style.animation =
`floatTag 4s ease-in-out ${index * 0.3}s infinite`;

}
);



/* =========================================
   BEST RESULT GLOW
========================================= */

const resultCard =
document.querySelector(
".best-result-card"
);

if(resultCard){

setInterval(()=>{

resultCard.classList.add(
"glow"
);

setTimeout(()=>{

resultCard.classList.remove(
"glow"
);

},1000);

},3000);

}



/* =========================================
   SMOOTH SECTION HIGHLIGHT
========================================= */

window.addEventListener(
"scroll",
() => {

const sections =
document.querySelectorAll(
".research-section"
);

sections.forEach(section => {

const rect =
section.getBoundingClientRect();

if(
rect.top < window.innerHeight * 0.4 &&
rect.bottom > 0
){

section.classList.add(
"section-active"
);

}else{

section.classList.remove(
"section-active"
);

}

});

}
);

/* =========================================
   ADVANCED CONVERGENCE VISUAL
========================================= */

const canvas =
document.getElementById(
"convergenceCanvas"
);

if(canvas){

const ctx =
canvas.getContext("2d");

canvas.width =
canvas.offsetWidth;

canvas.height =
canvas.offsetHeight;

const stages = [

1000,
200,
50,
10,
3,
1

];

const labels = [

"Generating Candidates",
"Distance Filtering",
"Turn Filtering",
"Risk Filtering",
"Top Candidates",
"Final Solution"

];

let stage = 0;

let particles = [];

function generateParticles(count){

particles = [];

for(let i=0;i<count;i++){

particles.push({

x:
Math.random()*
canvas.width,

y:
Math.random()*
canvas.height,

r:
Math.random()*3+1

});

}

}

generateParticles(
stages[0]
);

function draw(){

ctx.clearRect(
0,
0,
canvas.width,
canvas.height
);

particles.forEach(p=>{

ctx.beginPath();

ctx.arc(
p.x,
p.y,
p.r,
0,
Math.PI*2
);

ctx.fillStyle =
"rgba(139,160,255,0.9)";

ctx.fill();

});

requestAnimationFrame(
draw
);

}

draw();

function nextStage(){

stage++;

if(
stage >= stages.length
){

stage = 0;

}

document.getElementById(
"stageTitle"
).innerText =
labels[stage];

document.getElementById(
"stageCount"
).innerText =
stages[stage] +
" Candidates";

generateParticles(
Math.max(
stages[stage],
1
)
);

}

setInterval(
nextStage,
2200
);
}