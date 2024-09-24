# data_measurement_task

### Assumptions:

* Data is comming in one sample point at a time, like a real-time measuring device.
* If the 5 min interval was empty leave it empty. (Potential equipment failure).
* The incoming data can be trusted and is not malformed or corrupted.

### Usage

1. Clone repo
2. Insert test data into the input.txt file or which the target file in `solution.py`
3. Run the code, the output will be displayed in the console

```
python solution.py
```

### Implementation

For Measurement tracking I've created a MeasurementTracker class. With each new insert the class compares the new Measurement's time with the already existent data in the class and tracks the most recent reading for each 5 min interval.


The data format inside MeasurementTracker
```
data = {<MeasType>: {<timeStamp_1>: Measurement, <timeStamp_2>: Measurement}, <MeasType>: {}, ...}
```

This data storage way allows for easy return of a certain MeasType or returning all the data.

### Testing
For the testing of the class I've used the PyTest library and created the following tests:

* DateTime correction Testing:
    * tests if the time is not a multiple of 5 if it gets corrected to the closes future multiple of 5
    * tests if the time is a multiple of 5 minutes if it doens't change the time
* Empty Class Testing:
    * Empty MeasurementTracker for each MeasType returns empty list for GetOrderedData
    * Empty MeasurementTracker for each MeasType returns empty dictionary for getAllOrderedData
* One Item Testing:
    * Test if an item inserted into the MeasurementTracker retains all it's correct attributes and it's time gets adjusted to the correct time.
    * Test if the getAllOrderedData inserts Measurement in the correct category.
* Two Item Testing:
    * Tests if two different category Measurements inserted into the MeasurementTracker get inserted into different categories.
* Multiple Item ordering testing:
    * Tests if non conflicting 4 Measurements are ordered correctly
    * Tests if conflicting 4 Measurements are correctly ordered and chosen into timeframes
    * Tests if different category Measurements with conflicting times get ordered and inserted into their categories


**Note** the tests take a second to run, which is okay in this scenarion, but in bigger codebases would prob switch to not testing all possible permutations.