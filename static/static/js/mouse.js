//Mouse Dynamics
const mouseBiometrics = new Object(); // Set New Object

let xSpeed = new Array(); // Set array for caluculate x axis speed
let ySpeed = new Array(); // Set array for caluculate y axis speed
let xAsix = new Array(); // Set array for caluculate x axis
let yAxis = new Array(); // Set array for caluculate y axis
let distance = new Array(); // Set array for caluculate distance between two points
let buttonSpeed = new Array(); // Set array for caluculate button speed 
let scrollSpeed = new Array(); // Set array for scroll speed

let timeStamp = null;
let xTempAxis = null;
let yTempAxis = null;
let speed = 0

let startKey = {}
window.addEventListener('mousedown',function(event){
    const currentTime = Date.now(); //Select current date
    if (!startKey[event.button])
    {
        startKey[event.button] = currentTime; // Set current time on button down
    }
});
window.addEventListener('mouseup',function(event){
    const currentTime = Date.now(); // Select current date
    buttonHold = currentTime - startKey[event.button]; // Calculate hold time
    startKey[event.button] = null; // Set null for down button
    buttonSpeed.push(check(buttonHold)) // Add data to array
});
window.addEventListener('wheel',function(event){
    scrollDeltaY = Math.abs(event.deltaY); // Calculate Scroll speed
    scrollSpeed.push(check(scrollDeltaY)) // Add data to array
});

window.addEventListener('mousemove', function(event){
    // If null set the value to empty variables
    if(timeStamp == null)
    {
        timeStamp = Date.now();
        xTempAxis = event.x;
        yTempAxis = event.y;
    }
    else
    {
        let now = Date.now();
        let dateTime =  now - timeStamp; // Calculate time duration
        let xDistance = Math.abs(event.x - xTempAxis); // Calculate x distance
        let yDistance = Math.abs(event.y - yTempAxis); // Calculate y distance
        let xTempSpeed = Math.round(xDistance / dateTime * 100); // Calculate x temporary speed
        let yTempSpeed = Math.round(yDistance / dateTime * 100); // Calculate y temporary speed

        

        speed += Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2)); // Calculate Speed
        
        timeStamp = now; // Update with current timestamp
        xTempAxis = event.x; // Set current xAxis
        yTempAxis = event.y; // Set current yAxis

        xTempSpeed = check(xTempSpeed); // check for infinity or nan value
        yTempSpeed = check(yTempSpeed); // check for infinity or nan value
        eventX = check(event.x); // check for infinity or nan value
        eventY = check(event.y); // check for infinity or nan value
        speed = check(speed); // check for infinity or nan value

        xSpeed.push(xTempSpeed) // Add that data
        ySpeed.push(yTempSpeed); // Add that data
        xAsix.push(event.x); // Add that data
        yAxis.push(event.y); // Add that data
        distance.push(speed); // Add that data
    }
});
// Custom function to check infinity and NaN
function check(singelVal)
{
    if(isFinite(singelVal) == false )
    {
        if(isNaN(singelVal) == true)
        {
            return 0;
        }
        else
        {
            return singelVal;
        }
    }
    else
    {
        return singelVal;
    }
}
class MousedynamicS{
    constructor(){
        const xSpeedFeatures = new MouseFeatures(xSpeed); // Construct result on xspeed
        const ySpeedFeatures = new MouseFeatures(ySpeed); // Construct result on yspeed
        const xAxisFeatures = new MouseFeatures(xAsix);  // Construct result on xAxis
        const yAxisFeatures = new MouseFeatures(yAxis); // Construct result on yAxis
        const distanceFeatures = new MouseFeatures(distance); // Construct result on distacne
        const mouseButtonSpeed = new MouseFeatures(buttonSpeed); // Construct result on button speed
        const mouseScrollSpeed = new MouseFeatures(scrollSpeed); // Construct result on scrool speed

        // Get min,max,avg,std value for xSpeed
        mouseBiometrics['xSPeed_min'] = xSpeedFeatures.min();
        mouseBiometrics['xSPeed_max'] = xSpeedFeatures.max();
        mouseBiometrics['xSPeed_avg'] = xSpeedFeatures.avg();
        mouseBiometrics['xSPeed_std'] = xSpeedFeatures.std();

        // Get min,max,avg,std value for ySpeed
        mouseBiometrics['ySPeed_min'] = ySpeedFeatures.min();
        mouseBiometrics['ySPeed_max'] = ySpeedFeatures.max();
        mouseBiometrics['ySPeed_avg'] = ySpeedFeatures.avg();
        mouseBiometrics['ySPeed_std'] = ySpeedFeatures.std();

        // Get min,max,avg,std value for xAxis
        mouseBiometrics['xAxis_min'] = xAxisFeatures.min();
        mouseBiometrics['xAxis_max'] = xAxisFeatures.max();
        mouseBiometrics['xAxis_avg'] = xAxisFeatures.avg();
        mouseBiometrics['xAxis_std'] = xAxisFeatures.std();

        // Get min,max,avg,std value for yAxis
        mouseBiometrics['yFeatures_min'] = yAxisFeatures.min();
        mouseBiometrics['yFeatures_max'] = yAxisFeatures.max();
        mouseBiometrics['yFeatures_avg'] = yAxisFeatures.avg();
        mouseBiometrics['yFeatures_std'] = yAxisFeatures.std();

        // Get min,max,avg,std value for distance
        mouseBiometrics['distance_min'] = distanceFeatures.min();
        mouseBiometrics['distance_max'] = distanceFeatures.max();
        mouseBiometrics['distance_avg'] = distanceFeatures.avg();
        mouseBiometrics['distance_std'] = distanceFeatures.std();

        // Get min,max,avg,std value for button speed
        mouseBiometrics['button_speed_min'] = mouseButtonSpeed.min();
        mouseBiometrics['button_speed_max'] = mouseButtonSpeed.max();
        mouseBiometrics['button_speed_avg'] = mouseButtonSpeed.avg();
        mouseBiometrics['button_speed_std'] = mouseButtonSpeed.std();

        // Get min,max,avg,std value for scroll speed
        mouseBiometrics['scroll_speed_min'] = mouseScrollSpeed.min();
        mouseBiometrics['scroll_speed_max'] = mouseScrollSpeed.max();
        mouseBiometrics['scroll_speed_avg'] = mouseScrollSpeed.avg();
        mouseBiometrics['scroll_speed_std'] = mouseScrollSpeed.std();

        // Set values empty
        xSpeed = [];
        ySpeed = [];
        xAsix = [];
        yAxis = [];
        distance = [];
        buttonSpeed = [];
        scrollSpeed=[];
        timeStamp = null;
        xTempAxis = null;
        yTempAxis = null;
        speed = 0

        startKey.length = 0

        return mouseBiometrics; // Retunr dataset
    }
}
class MouseFeatures{
    constructor(dataset)
    {
     this.dataset = dataset // Get dataset
    }
    min()
    {
        // Calculate Min value from total dataset
        let currentData = this.dataset;
        let minVal = Math.min.apply(null,currentData);
        return this.validation(minVal);
    }
    max()
    {
        // Calculate Max value from total dataset
        let currentData = this.dataset;
        let maxVal = Math.max.apply(null,currentData)
        return this.validation(maxVal);
    }
    avg()
    {
        // Calculate average value from total dataset
        const currentData = this.dataset;
        const intial = 0;
        const average = parseFloat((currentData.reduce(this.sum, intial) / currentData.length));
        return this.validation(average);
    }
    std()
    {
        // Calculate Standard Deviation value from total dataset
        const currentData = this.dataset;
        const mean = this.avg();
        const intial = 0;
        const elementStd= currentData.map(val => Math.pow(val - mean, 2));
        const std = Math.sqrt(elementStd.reduce(this.sum, 0) * (1/currentData.length));
        return this.validation(std);
    }
    sum(value_1, value_2)
    {
        // Ssum two values
        return value_1 + value_2
    }
    // Custom validation function to check infinity and NaN
    validation(value)
    {
        if(isFinite(value) != false)
        {
            if(isNaN(value) != true)
            {
                return value;
            }
            else
            {
                value = 0;
                return value;
            }
                
        }
        else
        {
            value = 0;
            return value;
        } 
    }
}