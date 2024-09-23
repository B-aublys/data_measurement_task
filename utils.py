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
        self.data = {enum.value:{} for enum in MeasType}

        print(self.data)

    def dateTimeCorrection(self, timeStamp: float):
        if (remainder := timeStamp % 300) != 0:
            return timeStamp + timedelta(seconds=300 - remainder).total_seconds()
        return timeStamp

    def insert(self, measurement: Measurement):
        print(measurement.measurementTime)
        timeframe = self.dateTimeCorrection(measurement.measurementTime.timestamp())
        timedDada = self.data.get(timeframe)

        if not timedDada:
            self.data[timeframe] = {MeasType.SPO2: None,
                                    MeasType.HR:   None,
                                    MeasType.TEMP: None}

            self.data[timeframe][measurement.measurementType] = measurement
        else:
            data_point = self.data[timeframe][measurement.measurementType]
            if not data_point:
                self.data[timeframe][measurement.measurementType] = measurement
            elif self.data[timeframe][measurement.measurementType].measurementTime < measurement.measurementTime:
                self.data[timeframe][measurement.measurementType] = measurement

    # def getOrderedData(self):
    #     # TODO: return ordered data with changed timestamps to the new ones
    #     ordered_keys = sorted(self.data.keys())
    #     ordered_enums = {key: [] for enum in }

    #     pass


def inputLineToMeasurement(inputLine):
    line_list = inputLine[1:].rstrip('}\n').split(', ')
    return Measurement(datetime.fromisoformat(line_list[0]), MeasType[line_list[1]], float(line_list[2]))


if __name__ == '__main__':

    m_tracker = MeasurementTracker()

    with open('./input.txt') as inputFile:
        for line in inputFile:
            m_tracker.insert(inputLineToMeasurement(line))

    print(m_tracker.data)