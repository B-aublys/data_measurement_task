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
    """Tracks the latest Measurements for each 5min interval"""
    def __init__(self):
        self.data = {m_type:{} for m_type in MeasType}

    def dateTimeCorrection(self, timeStamp: float):
        """Converts the given timestamp to the closest future time that is divisable by 5 mins

           Ex. 2017-01-03T10:11:03 --> 2017-01-03T10:15:00
        """
        if (remainder := timeStamp % 300) != 0:
            return timeStamp + timedelta(seconds=300 - remainder).total_seconds()
        return timeStamp

    def insert(self, measurement: Measurement):
        """Inserts a given Measurement into the time-series"""
        timeframe = self.dateTimeCorrection(measurement.measurementTime.timestamp())
        timedDada = self.data[measurement.measurementType].get(timeframe)

        if not timedDada or timedDada.measurementTime < measurement.measurementTime:
            self.data[measurement.measurementType][timeframe] = measurement

    def getOrderedData(self, m_type: MeasType):
        """Returns a time ordered Measurement list of a specific MeasType"""
        return_data = []

        if not self.data.get(m_type):
            return []

        for key in sorted(self.data[m_type].keys()):
            data_point = self.data[m_type][key]
            data_point.measurementTime = datetime.fromtimestamp(key)
            return_data.append(data_point)
        return return_data

    def getAllOrderedData(self):
        """Returns a dictionary containing all inputed MeasType time ordered lists of Measurements

           return type:
           data{<MeasType_1>:[Measurement, ...], <MeasType_2>:[],...}
        """
        return_data = {}
        for m_type in MeasType:
            return_data[m_type] = self.getOrderedData(m_type)
        return return_data


def inputLineToMeasurement(inputLine):
    """Converts the challenge given input line str to a Measurement object

       Input Ex. '{2017-01-03T10:10:00, SPO2, 95.08}'
    """
    line_list = inputLine[1:].rstrip('}\n').split(', ')
    return Measurement(datetime.fromisoformat(line_list[0]), MeasType[line_list[1]], float(line_list[2]))

def measurementToOutputLine(measurement: Measurement):
    """Converts a Measurement to the challange given output line str

       Output Ex. '{2017-01-03T10:10:00, TEMP, 35.01}'
    """
    return f'{{{measurement.measurementTime.isoformat()}, {measurement.measurementType.name}, {measurement.value}}}'