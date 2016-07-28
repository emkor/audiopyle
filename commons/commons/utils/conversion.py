import calendar
import math
from datetime import datetime


def b_to_B(b):
    return math.ceil(b / 8.0)


def B_to_b(B):
    return int(B * 8)


def to_kilo(v):
    return v / 1000.0


def to_mega(v):
    return v / 1000000.0


def frames_to_sec(frames, sample_rate):
    return float(frames) / float(sample_rate)


def sec_to_frames(seconds, sample_rate):
    return int(sample_rate * seconds)


def sec_to_min(sec):
    return float(sec) / float(60)


def min_to_sec(minutes):
    return minutes * 60


def utc_datetime_to_timestamp(dt):
    return calendar.timegm(dt.utctimetuple())


def utc_timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp)
