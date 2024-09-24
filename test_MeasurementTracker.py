import pytest
from utils import *
from datetime import datetime, timedelta
import itertools

@pytest.fixture
def MTracker():
    return MeasurementTracker()

@pytest.fixture
def datetimeA():
    return datetime.fromisoformat('2017-01-03T10:05:01')

@pytest.fixture
def datetimeACorrected():
    return datetime.fromisoformat('2017-01-03T10:10:00')

@pytest.fixture
def measurementSPO2(datetimeA):
    return Measurement(datetimeA, MeasType.SPO2, 95.1)

@pytest.fixture
def measurementHR(datetimeA):
    return Measurement(datetimeA, MeasType.HR, 80)

@pytest.fixture
def measurementSPO2TimeCorrected(measurementSPO2, datetimeACorrected):
    measurementSPO2.measurementTime = datetimeACorrected
    return measurementSPO2

@pytest.fixture
def fourOrderedMeasurementsSPO2(datetimeA):
    return [Measurement(datetimeA, MeasType.SPO2, 0),
            Measurement(datetimeA + timedelta(minutes=5), MeasType.SPO2, 1),
            Measurement(datetimeA + timedelta(minutes=10), MeasType.SPO2, 2),
            Measurement(datetimeA + timedelta(minutes=15), MeasType.SPO2, 3),]

# NOTE: the corrected values that should stay are 1 and 3
@pytest.fixture
def fourConflictingTEMPMeasurements(datetimeA):
    return [Measurement(datetimeA, MeasType.TEMP, 0),
            Measurement(datetimeA + timedelta(minutes=2, seconds=1), MeasType.TEMP, 1),
            Measurement(datetimeA + timedelta(minutes=10), MeasType.TEMP, 2),
            Measurement(datetimeA + timedelta(minutes=11), MeasType.TEMP, 3),]



# dateTimeCorrection Tests -----------------------------------------------------------------
def test_dateTimeCorrectionTimeAddition(MTracker, datetimeA, datetimeACorrected):
    """tests if the time is not a multiple of 5 if it gets corrected to the closes future multiple of 5"""
    datetimeAT = datetimeA.timestamp()
    datetimeACorrectedT = datetimeACorrected.timestamp()

    for seconds in range(300):
        assert MTracker.dateTimeCorrection(datetimeAT) == datetimeACorrectedT
        datetimeAT += 1

def test_dateTimeCorrectionNotChaningTime(MTracker, datetimeACorrected):
    """tests if the time is a multiple of 5 minutes if it doens't change the time"""
    datetimeCorrectedT = datetimeACorrected.timestamp()
    assert MTracker.dateTimeCorrection(datetimeCorrectedT) == datetimeCorrectedT


# Empty MeasurementTracker Tests -----------------------------------------------------------
def test_getOrederedDataEmpty(MTracker):
    """Empty MeasurementTracker for each MeasType returns empty list for GetOrderedData"""
    for mType in MeasType:
        assert MTracker.getOrderedData(mType) == []

def test_getAllOrederedDataEmpty(MTracker):
    """Empty MeasurementTracker for each MeasType returns empty dictionary for getAllOrderedData"""
    assert MTracker.getAllOrderedData() == {}


# One Item MeasurementTracker Tests --------------------------------------------------------
def test_getOrderedDataOneItem(MTracker, measurementSPO2, measurementSPO2TimeCorrected):
    """Test if an item inserted into the MeasurementTracker retains all it's correct attributes
       and it's time gets adjusted to the correct time.
    """
    MTracker.insert(measurementSPO2)
    assert len(MTracker.getOrderedData(measurementSPO2.measurementType)) == 1

    dataPoint = MTracker.getOrderedData(measurementSPO2.measurementType)[0]
    assert dataPoint.measurementTime == measurementSPO2TimeCorrected.measurementTime
    assert dataPoint.measurementType == measurementSPO2TimeCorrected.measurementType
    assert dataPoint.value == measurementSPO2TimeCorrected.value

def test_getAllOrderedDataOneItem(MTracker, measurementSPO2):
    """Test if the getAllOrderedData inserts Measurement in the correct category"""
    MTracker.insert(measurementSPO2)

    assert len(MTracker.getAllOrderedData().keys()) == 1
    assert list(MTracker.getAllOrderedData().keys())[0] == measurementSPO2.measurementType


# Two Item getAllOrderedData Test
def test_GetAllOrderedDataTwoItems(MTracker, measurementSPO2, measurementHR):
    """Tests if two different category Measurements inserted into the MeasurementTracker
       get inserted into different categories.
    """
    MTracker.insert(measurementSPO2)
    MTracker.insert(measurementHR)

    assert (set(MTracker.getAllOrderedData().keys()) ==
            set([measurementHR.measurementType, measurementSPO2.measurementType]))


# Multiple Item correct ordering ----------------------------------------------------------
def test_correctFourItemOrdering(fourOrderedMeasurementsSPO2):
    """Tests if non conflicting 4 Measurements are ordered correctly"""
    allPermutations = itertools.permutations(fourOrderedMeasurementsSPO2)

    for permutation in allPermutations:
        MTracker = MeasurementTracker()
        for measurement in permutation:
            MTracker.insert(measurement)

        assert len(MTracker.getOrderedData(MeasType.SPO2)) == 4
        assert MTracker.getOrderedData(MeasType.SPO2)[0].value == 0
        assert MTracker.getOrderedData(MeasType.SPO2)[1].value == 1
        assert MTracker.getOrderedData(MeasType.SPO2)[2].value == 2
        assert MTracker.getOrderedData(MeasType.SPO2)[3].value == 3

def test_correctConflictingFourItemOrdering(fourConflictingTEMPMeasurements):
    """Tests if conflicting 4 Measurements are correctly ordered and chosen into 2 timeframes"""
    allPermutations = itertools.permutations(fourConflictingTEMPMeasurements)

    for permutation in allPermutations:
        MTracker = MeasurementTracker()
        for measurement in permutation:
            MTracker.insert(measurement)

        assert len(MTracker.getOrderedData(MeasType.TEMP)) == 2
        assert MTracker.getOrderedData(MeasType.TEMP)[0].value == 1
        assert MTracker.getOrderedData(MeasType.TEMP)[1].value == 3


# Note: this takes a second or so maybe in a bigger test db would replace with something faster
def test_SPO2andTempFourItemOrdering(MTracker, fourOrderedMeasurementsSPO2, fourConflictingTEMPMeasurements):
    """Tests inserting all possible 4 Temp and 2 SPO2 Measurements order permutations"""
    fourConflictingTEMPMeasurements.extend(fourOrderedMeasurementsSPO2)
    allPermutations = itertools.permutations(fourConflictingTEMPMeasurements)

    for permutation in allPermutations:
        MTracker = MeasurementTracker()
        for measurement in permutation:
            MTracker.insert(measurement)

        allData = MTracker.getAllOrderedData()
        assert len(list(allData.keys())) == 2
        assert len(list(allData[MeasType.TEMP])) == 2
        assert len(list(allData[MeasType.SPO2])) == 4

        assert allData[MeasType.TEMP][0].value == 1
        assert allData[MeasType.TEMP][1].value == 3

        assert allData[MeasType.SPO2][0].value == 0
        assert allData[MeasType.SPO2][1].value == 1
        assert allData[MeasType.SPO2][2].value == 2
        assert allData[MeasType.SPO2][3].value == 3