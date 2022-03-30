from datetime import datetime

_POWER_SENSOR_ENDPOINT = "/sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0//in_power0_input"

_SEQUENCES = []
_DATA_POINTS = []
_kill = False


def send_kill():
    global _kill
    _kill = True


class _DataPoint:
    relative_time: datetime
    power: int
    sequence: any = None

    def __init__(self, relative_time: datetime, power: int, sequence=None):
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


def measure_continuous(sequence=None):
    print("Started measuring")
    global _kill
    while not _kill:
        measure(sequence)
    _kill = False
    print("Stopped measuring")


def clean():
    global _SEQUENCES
    global _DATA_POINTS
    _SEQUENCES = []
    _DATA_POINTS = []


if __name__ == "__main__":
    pass
