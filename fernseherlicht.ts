const powerDevice = "hm-rpc.0.0001DD8993E6E2.6.POWER";
const lightDevice = "hm-rpc.0.0001DD8993E6E2.3.STATE";

let controlledByTv = false;

setInterval(() => {
    const powerConsumption = getState(powerDevice).val;

    if(powerConsumption > 20) {
        setState(lightDevice, true);
        controlledByTv = true;
    } else if (controlledByTv) {
        setState(lightDevice, false);
        controlledByTv = false;
    }
}, 1000);
