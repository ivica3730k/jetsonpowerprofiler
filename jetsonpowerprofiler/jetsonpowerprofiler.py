from datetime import datetime
from datetime import time

_POWER_SENSOR_ENDPOINT = "/sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0//in_power0_input"

_SEQUENCES = []
_DATA_POINTS = []


class _DataPoint:
    relative_time: time
    power: int
    sequence: any = None

    def __init__(self, relative_time: time, power: int, sequence=None):
        self.relative_time = relative_time
        self.power = power
        self.sequence = sequence


def measure(sequence=None):
    now = datetime.now()
    file = open(_POWER_SENSOR_ENDPOINT)
    power = file.read()
    power = int(power)
    data_point = _DataPoint(now, power, sequence)
    if sequence:
        if sequence not in _SEQUENCES:
            _SEQUENCES.append(sequence)
    _DATA_POINTS.append(data_point)


def get_average_power():
    total = 0
    for i in _DATA_POINTS:
        i: _DataPoint
        total += i.power
    return total / len(_DATA_POINTS)


def get_total_measuring_time():
    first: _DataPoint = _DATA_POINTS[0]
    last: _DataPoint = _DATA_POINTS[-1]
    timedelta = last.relative_time - first.relative_time
    return timedelta.total_seconds()


if __name__ == "__main__":
    pass
