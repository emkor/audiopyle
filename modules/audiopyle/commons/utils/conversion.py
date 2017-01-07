import calendar
import math
from datetime import datetime


def b_to_B(b):
    """
    Bits to bytes
    :type b: int
    :rtype: int
    """
    return math.ceil(b / 8.0)


def B_to_b(B):
    """
    Bytes to bits
    :type B: int
    :rtype: int
    """
    return int(B * 8)


def to_kilo(v):
    """
    Converts to kilo (thousands)
    :type v: float
    :rtype: float
    """
    return v / 1000.0


def to_mega(v):
    """
    Converts to mega (millions)
    :type v: float
    :rtype: float
    """
    return v / 1000000.0


def frames_to_sec(frames_count, sample_rate):
    """
    Converts frames count to seconds using sample rate
    :type frames_count: int
    :type sample_rate: int
    :rtype: float
    """
    return float(frames_count) / float(sample_rate)


def sec_to_frames(seconds, sample_rate):
    """
    Converts seconds to frames count
    :type seconds: float
    :type sample_rate: int
    :rtype: int
    """
    return round(sample_rate * seconds)


def sec_to_min(sec):
    """
    Converts seconds to minutes with decimal fraction
    :type sec: float
    :rtype: float
    """
    return float(sec) / float(60)


def min_to_sec(minutes):
    """
    Converts minutes to seconds
    :type minutes: float
    :rtype: float
    """
    return minutes * 60.0


def utc_datetime_to_timestamp(dt):
    """
    Converts datetime (UTC) to Unix timestamp
    :type dt: datetime
    :rtype: int
    """
    return calendar.timegm(dt.utctimetuple())


def utc_timestamp_to_datetime(timestamp):
    """
    Converts timestamp (seconds) to UTC datetime
    :type timestamp: float | int
    :rtype: datetime
    """
    return datetime.utcfromtimestamp(round(timestamp))
