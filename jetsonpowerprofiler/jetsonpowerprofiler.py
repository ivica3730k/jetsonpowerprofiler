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

    def __float__(self):
        return self.power

    def __repr__(self):
        return self.power


def measure(sequence=None):
    now = datetime.now().time()  # time object
    file = open(_POWER_SENSOR_ENDPOINT)
    power = file.read()
    data_point = _DataPoint(now, power, sequence)
    if sequence:
        if sequence not in _SEQUENCES:
            _SEQUENCES.append(sequence)
    _DATA_POINTS.append(data_point)


def get_average_power():
    return sum(_DATA_POINTS) / len(_DATA_POINTS)


if __name__ == "__main__":
    pass