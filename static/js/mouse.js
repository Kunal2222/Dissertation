//Mouse Dynamics
const mouseBiometrics = new Object();

let xSpeed = new Array();
let ySpeed = new Array();
let xAsix = new Array();
let yAxis = new Array();
let distance = new Array();
let buttonSpeed = new Array();
let scrollSpeed = new Array();

let timeStamp = null;
let xTempAxis = null;
let yTempAxis = null;
let speed = 0

let startKey = {}
window.addEventListener('mousedown',function(event){
    console.log(event.button)
    const currentTime = Date.now();
    if (!startKey[event.button])
    {
        startKey[event.button] = currentTime;
    }
});
window.addEventListener('mouseup',function(event){
    const currentTime = Date.now();
    buttonHold = currentTime - startKey[event.button];
    startKey[event.button] = null;
    buttonSpeed.push(check(buttonHold))
});
window.addEventListener('wheel',function(event){
    scrollDeltaY = Math.abs(event.deltaY);
    scrollSpeed.push(check(scrollDeltaY))
});

window.addEventListener('mousemove', function(event){
    if(timeStamp == null)
    {
        timeStamp = Date.now();
        xTempAxis = event.x;
        yTempAxis = event.y;
    }
    else
    {
        let now = Date.now();
        let dateTime =  now - timeStamp;
        let xDistance = Math.abs(event.x - xTempAxis);
        let yDistance = Math.abs(event.y - yTempAxis);
        let xTempSpeed = Math.round(xDistance / dateTime * 100);
        let yTempSpeed = Math.round(yDistance / dateTime * 100);

        

        speed += Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        
        timeStamp = now;
        xTempAxis = event.x;
        yTempAxis = event.y;

        xTempSpeed = check(xTempSpeed);
        yTempSpeed = check(yTempSpeed);
        eventX = check(event.x);
        eventY = check(event.y);
        speed = check(speed);

        xSpeed.push(xTempSpeed)
        ySpeed.push(yTempSpeed);
        xAsix.push(event.x);
        yAxis.push(event.y);
        distance.push(speed);
    }
});
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
        const xSpeedFeatures = new MouseFeatures(xSpeed);
        const ySpeedFeatures = new MouseFeatures(ySpeed);
        const xAxisFeatures = new MouseFeatures(xAsix);
        const yAxisFeatures = new MouseFeatures(yAxis);
        const distanceFeatures = new MouseFeatures(distance);
        const mouseButtonSpeed = new MouseFeatures(buttonSpeed);
        const mouseScrollSpeed = new MouseFeatures(scrollSpeed)

        mouseBiometrics['xSPeed_min'] = xSpeedFeatures.min();
        mouseBiometrics['xSPeed_max'] = xSpeedFeatures.max();
        mouseBiometrics['xSPeed_avg'] = xSpeedFeatures.avg();
        mouseBiometrics['xSPeed_std'] = xSpeedFeatures.std();

        mouseBiometrics['ySPeed_min'] = ySpeedFeatures.min();
        mouseBiometrics['ySPeed_max'] = ySpeedFeatures.max();
        mouseBiometrics['ySPeed_avg'] = ySpeedFeatures.avg();
        mouseBiometrics['ySPeed_std'] = ySpeedFeatures.std();

        mouseBiometrics['xAxis_min'] = xAxisFeatures.min();
        mouseBiometrics['xAxis_max'] = xAxisFeatures.max();
        mouseBiometrics['xAxis_avg'] = xAxisFeatures.avg();
        mouseBiometrics['xAxis_std'] = xAxisFeatures.std();

        mouseBiometrics['yFeatures_min'] = yAxisFeatures.min();
        mouseBiometrics['yFeatures_max'] = yAxisFeatures.max();
        mouseBiometrics['yFeatures_avg'] = yAxisFeatures.avg();
        mouseBiometrics['yFeatures_std'] = yAxisFeatures.std();

        mouseBiometrics['distance_min'] = distanceFeatures.min();
        mouseBiometrics['distance_max'] = distanceFeatures.max();
        mouseBiometrics['distance_avg'] = distanceFeatures.avg();
        mouseBiometrics['distance_std'] = distanceFeatures.std();

        mouseBiometrics['button_speed_min'] = mouseButtonSpeed.min();
        mouseBiometrics['button_speed_max'] = mouseButtonSpeed.max();
        mouseBiometrics['button_speed_avg'] = mouseButtonSpeed.avg();
        mouseBiometrics['button_speed_std'] = mouseButtonSpeed.std();

        mouseBiometrics['scroll_speed_min'] = mouseScrollSpeed.min();
        mouseBiometrics['scroll_speed_max'] = mouseScrollSpeed.max();
        mouseBiometrics['scroll_speed_avg'] = mouseScrollSpeed.avg();
        mouseBiometrics['scroll_speed_std'] = mouseScrollSpeed.std();

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

        return mouseBiometrics;
    }
}
class MouseFeatures{
    constructor(dataset)
    {
     this.dataset = dataset
    }
    min()
    {
        let currentData = this.dataset;
        let minVal = Math.min.apply(null,currentData);
        return this.validation(minVal);
    }
    max()
    {
        let currentData = this.dataset;
        let maxVal = Math.max.apply(null,currentData)
        return this.validation(maxVal);
    }
    avg()
    {
        const currentData = this.dataset;
        const intial = 0;
        const average = parseFloat((currentData.reduce(this.sum, intial) / currentData.length));
        return this.validation(average);
    }
    std()
    {
        const currentData = this.dataset;
        const mean = this.avg();
        const intial = 0;
        const elementStd= currentData.map(val => Math.pow(val - mean, 2));
        const std = Math.sqrt(elementStd.reduce(this.sum, 0) * (1/currentData.length));
        return this.validation(std);
    }
    sum(value_1, value_2)
    {
        return value_1 + value_2
    }
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