//User Datasets
const userBiometrics = new Object();
let keyHold = new Array();
let keyDownLatency = new Array();
let keyUpLatency = new Array();
let keyUpDown = new Array();
let keyDownUp = new Array();

// Temporary Variables
const startKey = {};
const keyDownDistance = Array();
const keyUpDistance = Array();

const user = 1;
document.getElementById("wrttingPad").addEventListener("keydown", function(event){
    const currentTime = Date.now();  
    const keyDownDistanceCount = keyDownDistance.length; // Length of key down distance
    const keyUpDistanceCount = keyUpDistance.length; // Length of key up up time
    if(keyDownDistanceCount > 0)
    {
        twoKeyDistance = currentTime - keyDownDistance[keyDownDistanceCount-1]; // Calcualte key down down time
        keyDownLatency.push(twoKeyDistance); // push key down down time
    }
    if(keyUpDistanceCount > 0)
    {
        upDownDistance = currentTime - keyUpDistance[keyUpDistanceCount-1]; // Calculate up down time
        keyUpDown.push(upDownDistance); // push key up down time
    }
    keyDownDistance.push(currentTime);
    if (!startKey[event.key])
    {
        startKey[event.key] = currentTime; // Add current down key and time
    }
});
document.getElementById("wrttingPad").addEventListener("keyup", function(event){
    const currentTime = Date.now(); // Current time
    const keyUpDistanceCount = keyUpDistance.length; // Length of key up distacne
    const keyDownDistanceCount = keyDownDistance.length; // Length of key down distance 
    if(keyUpDistanceCount > 0)
    {
        twoKeyDistance = currentTime - keyUpDistance[keyUpDistanceCount-1]; // Calulet up up time
        keyUpLatency.push(twoKeyDistance); // Push up up time
    }
    if(keyDownDistanceCount > 1)
    {
        downUpDistance = currentTime - keyDownDistance[keyDownDistanceCount-2]; // Calculate Down up time
        keyDownUp.push(downUpDistance); // Push down up 
    }
    keyUpDistance.push(currentTime); // Updaing the keyup stack
    keyHoldTime = currentTime - startKey[event.key]; // Calulate key hold time
    startKey[event.key] = null; // Set downkey value null
    if(isNaN(keyHoldTime) == false)
    {
        keyHold.push(keyHoldTime); // Push the keyhold time to array
    }
});

/*Set Interverl for every minute or second to detect the biometrics*/
class Keystrock{
    constructor(){
        const keyHoldFeatures = new Features(keyHold); // Caling constructor
        const downDownFeatures = new Features(keyDownLatency); // Caling constructor
        const upUpFeatures = new Features(keyUpLatency); // Caling constructor
        const upDownFeatures = new Features(keyUpDown); // Caling constructor
        const downUpFeatures = new Features(keyDownUp); // Caling constructor

        // Get Min, Max, Avg, Std for Hold Min Values
        userBiometrics['hold_min'] = keyHoldFeatures.min();
        userBiometrics['hold_max'] = keyHoldFeatures.max();
        userBiometrics['hold_avg'] = keyHoldFeatures.avg();
        userBiometrics['hold_std'] = keyHoldFeatures.std();

        // Get Min, Max, Avg, Std for Down Down Values
        userBiometrics['down_down_min'] = downDownFeatures.min();
        userBiometrics['down_down_max'] = downDownFeatures.max();
        userBiometrics['down_down_avg'] = downDownFeatures.avg();
        userBiometrics['down_down_std'] = downDownFeatures.std();

        // Get Min, Max, Avg, Std for Up Up Values
        userBiometrics['up_up_min'] = upUpFeatures.min();
        userBiometrics['up_up_max'] = upUpFeatures.max();
        userBiometrics['up_up_avg'] = upUpFeatures.avg();
        userBiometrics['up_up_std'] = upUpFeatures.std();

        // Get Min, Max, Avg, Std for Up Down Values
        userBiometrics['up_down_min'] = upDownFeatures.min();
        userBiometrics['up_down_max'] = upDownFeatures.max();
        userBiometrics['up_down_avg'] = upDownFeatures.avg();
        userBiometrics['up_down_std'] = upDownFeatures.std();

        // Get Min, Max, Avg, Std for Down Up Values
        userBiometrics['down_up_min'] = downUpFeatures.min();
        userBiometrics['down_up_max'] = downUpFeatures.max();
        userBiometrics['down_up_avg'] = downUpFeatures.avg();
        userBiometrics['down_up_std'] = downUpFeatures.std();

        //Set Values empty
        keyHold = [];
        keyDownLatency = [];
        keyUpLatency = [];
        keyUpDown = [];
        keyDownUp = [];

        startKey.length = 0;
        keyDownDistance.length = 0;
        keyUpDistance.length = 0;

        return userBiometrics; // Returning the dataset
    }
}
class Features{
    constructor(dataset)
    {
     this.dataset = dataset // Get the dataset
    }
    min()
    {
        // Calculate min value for dataset
        let currentData = this.dataset;
        let minVal = Math.min.apply(null,currentData);
        return this.validation(minVal);
    }
    max()
    {
        // Calcualate max value for dataset
        let currentData = this.dataset;
        let maxVal = Math.max.apply(null,currentData)
        
        return this.validation(maxVal);
    }
    avg()
    {
        // Calculating Average for datasets
        const currentData = this.dataset;
        const intial = 0;
        const average = parseFloat((currentData.reduce(this.sum, intial) / currentData.length));
        return this.validation(average);
    }
    std()
    {
        // Calculating Standard Deviation
        const currentData = this.dataset;
        const mean = this.avg();
        const intial = 0;
        const elementStd= currentData.map(val => Math.pow(val - mean, 2));
        const std = Math.sqrt(elementStd.reduce(this.sum, 0) * (1/currentData.length));
        return this.validation(std);
    }
    // Custom total funciton of two value
    sum(value_1, value_2)
    {
        return value_1 + value_2
    }
    // Custom validation function
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