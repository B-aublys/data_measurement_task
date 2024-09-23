# data_measurement_task


## Algorythm idea

### Assumptions:

* Data is comming in one sample point at a time, like a real-time measuring device.
* If the 5 min interval was empty leave it empty. (Potential equipment failure)
* All the data can be stored in memory.

 ### Implementation

 To not over-complicated or over-analyse the problem I have decided on a simple implementation based on a dictionary where the key is the time at which the reading was taken and the value is another dictionary storing the Measurements. Furthermore the lowest and highest times will be logged for usage simplicty.

 ```
 data = { time1: {SPO2: Measurement{}, HR:..., TEMP:...}, time2: {}, ...}
 ```

