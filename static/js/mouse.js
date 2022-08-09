const xAxis = new Array();
const yAxis = new Array();
const timestamp = new Array();
const accelarator = new Array();
const jerk = new Array();
const type = new Array();
const button = new Array();

window.addEventListener('mousemove', function(event){
    x = event.x;
    y = event.y;
    timestap = Date.now();
    console.log(`Mouse Asix X:${event.x}, Y:${event.y}, Timestamp:${timestap}`)
});