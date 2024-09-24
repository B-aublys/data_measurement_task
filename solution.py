from utils import MeasurementTracker, inputLineToMeasurement, measurementToOutputLine

if __name__ == '__main__':
    m_tracker = MeasurementTracker()

    with open('./input.txt') as inputFile:
        for line in inputFile:
            m_tracker.insert(inputLineToMeasurement(line))

    all_data = m_tracker.getAllOrderedData()
    for key in all_data.keys():
        for measurement in all_data[key]:
            print(measurementToOutputLine(measurement))
