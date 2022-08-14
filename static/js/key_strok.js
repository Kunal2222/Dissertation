//User Datasets
const userBiometrics = new Object();
let keyHold = new Array();
let keyDownLatency = new Array();
let keyUpLatency = new Array();
let keyUpDown = new Array();
let keyDownUp = new Array();

const startKey = {};
const keyDownDistance = Array();
const keyUpDistance = Array();

const user = 1;
document.getElementById("wrttingPad").addEventListener("keydown", function(event){
    const currentTime = Date.now();
    const keyDownDistanceCount = keyDownDistance.length;
    const keyUpDistanceCount = keyUpDistance.length;
    if(keyDownDistanceCount > 0)
    {
        twoKeyDistance = currentTime - keyDownDistance[keyDownDistanceCount-1];
        keyDownLatency.push(twoKeyDistance);
    }
    if(keyUpDistanceCount > 0)
    {
        upDownDistance = currentTime - keyUpDistance[keyUpDistanceCount-1];
        keyUpDown.push(upDownDistance);
    }
    keyDownDistance.push(currentTime);
    if (!startKey[event.key])
    {
        startKey[event.key] = currentTime;
    }
});
document.getElementById("wrttingPad").addEventListener("keyup", function(event){
    const currentTime = Date.now();
    const keyUpDistanceCount = keyUpDistance.length;
    const keyDownDistanceCount = keyDownDistance.length;
    if(keyUpDistanceCount > 0)
    {
        twoKeyDistance = currentTime - keyUpDistance[keyUpDistanceCount-1];
        keyUpLatency.push(twoKeyDistance);
    }
    if(keyDownDistanceCount > 1)
    {
        downUpDistance = currentTime - keyDownDistance[keyDownDistanceCount-2];
        keyDownUp.push(downUpDistance);
    }
    keyUpDistance.push(currentTime);
    keyHoldTime = currentTime - startKey[event.key];
    startKey[event.key] = null;
    if(isNaN(keyHoldTime) == false)
    {
        keyHold.push(keyHoldTime);
    }
});

/*Set Interverl for every minute or second to detect the biometrics*/
class Keystrock{
    constructor(user){
        const keyHoldFeatures = new Features(keyHold);
        const downDownFeatures = new Features(keyDownLatency);
        const upUpFeatures = new Features(keyUpLatency);
        const upDownFeatures = new Features(keyUpDown);
        const downUpFeatures = new Features(keyDownUp);

        userBiometrics['hold_min'] = keyHoldFeatures.min();
        userBiometrics['hold_max'] = keyHoldFeatures.max();
        userBiometrics['hold_avg'] = keyHoldFeatures.avg();
        userBiometrics['hold_std'] = keyHoldFeatures.std();

        userBiometrics['down_down_min'] = downDownFeatures.min();
        userBiometrics['down_down_max'] = downDownFeatures.max();
        userBiometrics['down_down_avg'] = downDownFeatures.avg();
        userBiometrics['down_down_std'] = downDownFeatures.std();

        userBiometrics['up_up_min'] = upUpFeatures.min();
        userBiometrics['up_up_max'] = upUpFeatures.max();
        userBiometrics['up_up_avg'] = upUpFeatures.avg();
        userBiometrics['up_up_std'] = upUpFeatures.std();


        userBiometrics['up_down_min'] = upDownFeatures.min();
        userBiometrics['up_down_max'] = upDownFeatures.max();
        userBiometrics['up_down_avg'] = upDownFeatures.avg();
        userBiometrics['up_down_std'] = upDownFeatures.std();

        userBiometrics['down_up_min'] = downUpFeatures.min();
        userBiometrics['down_up_max'] = downUpFeatures.max();
        userBiometrics['down_up_avg'] = downUpFeatures.avg();
        userBiometrics['down_up_std'] = downUpFeatures.std();

        keyHold = [];
        keyDownLatency = [];
        keyUpLatency = [];
        keyUpDown = [];
        keyDownUp = [];

        return userBiometrics;
    }
}
class Features{
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