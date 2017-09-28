import calendar
import math
from datetime import datetime
from typing import Text, Any, Type, List


def b_to_B(b: float) -> int:
    return int(math.ceil(b / 8.0))


def B_to_b(B: float) -> int:
    return int(B * 8)


def to_kilo(v: float) -> float:
    return v / 1000.0


def to_mega(v: float) -> float:
    return v / 1000000.0


def frames_to_sec(frames_count: int, sample_rate: int) -> float:
    """Converts frames count to seconds using sample rate"""
    return float(frames_count) / float(sample_rate)


def sec_to_frames(seconds: float, sample_rate: int) -> int:
    """Converts seconds to frames count"""
    return round(sample_rate * seconds)


def sec_to_min(sec: float) -> float:
    """Converts seconds to minutes with decimal fraction"""
    return float(sec) / float(60)


def min_to_sec(minutes: float) -> float:
    """Converts minutes to seconds"""
    return minutes * 60.0


def utc_datetime_to_timestamp(dt: datetime) -> int:
    """Converts datetime (UTC) to Unix timestamp"""
    return calendar.timegm(dt.utctimetuple())


def utc_timestamp_to_datetime(timestamp: float) -> datetime:
    """Converts timestamp (seconds) to UTC datetime"""
    return datetime.utcfromtimestamp(round(timestamp))


def normalize(text: Text) -> Text:
    return text.lower().strip()


def seconds_between(start_time_point: datetime, end_time_point: datetime = datetime.utcnow(), precision: int = 2):
    return round((end_time_point - start_time_point).total_seconds(), precision)


def safe_cast(value: Any, expected_type: Type, default: Any = None) -> Any:
    try:
        return expected_type(value)
    except ValueError:
        return default


def first_element_or(collection, default=None):
    # type: (List[Any], Any) -> Any
    return collection[0] if len(collection) else default
