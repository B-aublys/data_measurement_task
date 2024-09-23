from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3


@dataclass
class Measurement:
    measurementTime: datetime = datetime.min
    measurementType: MeasType = MeasType.SPO2
    value: float = 0.0


class MeasurementTracker():
    def __init__(self):
        self.data = {m_type:{} for m_type in MeasType}

    def dateTimeCorrection(self, timeStamp: float):
        if (remainder := timeStamp % 300) != 0:
            return timeStamp + timedelta(seconds=300 - remainder).total_seconds()
        return timeStamp

    def insert(self, measurement: Measurement):
        timeframe = self.dateTimeCorrection(measurement.measurementTime.timestamp())
        timedDada = self.data[measurement.measurementType].get(timeframe)

        if not timedDada or timedDada.measurementTime < measurement.measurementTime:
            self.data[measurement.measurementType][timeframe] = measurement

    def getOrderedData(self, m_type: MeasType):
        return_data = []
        for key in sorted(self.data[m_type].keys()):
            data_point = self.data[m_type][key]
            data_point.measurementTime = datetime.fromtimestamp(key)
            return_data.append(data_point)
        return return_data

    def getAllOrderedData(self):
        return_data = {}
        for m_type in MeasType:
            return_data[m_type] = self.getOrderedData(m_type)
        return return_data


def inputLineToMeasurement(inputLine):
    line_list = inputLine[1:].rstrip('}\n').split(', ')
    return Measurement(datetime.fromisoformat(line_list[0]), MeasType[line_list[1]], float(line_list[2]))


if __name__ == '__main__':

    m_tracker = MeasurementTracker()

    with open('./input.txt') as inputFile:
        for line in inputFile:
            m_tracker.insert(inputLineToMeasurement(line))

    print(m_tracker.getAllOrderedData())