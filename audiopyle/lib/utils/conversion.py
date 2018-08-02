import calendar
import math
from datetime import datetime
from typing import Text, Any, Type, List, Union

from pympler.asizeof import asizeof

ISO_8601_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


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


def utc_datetime_to_iso_format(dt: datetime) -> Text:
    """Converts datetime (UTC) to ISO 8601 format"""
    return dt.strftime(ISO_8601_TIME_FORMAT)


def utc_iso_format_to_datetime(iso_dt: Text) -> datetime:
    """Converts ISO 8601 formatted UTC date string to datetime"""
    return datetime.strptime(iso_dt, ISO_8601_TIME_FORMAT)


def normalize(text: Text) -> Text:
    return text.lower().strip()


def seconds_between(start_time_point: datetime, end_time_point: datetime = None, precision: int = 3):
    end_time_point = end_time_point or datetime.utcnow()
    return round((end_time_point - start_time_point).total_seconds(), precision)


def safe_cast(value: Any, expected_type: Type, default: Any = None) -> Any:
    if value is None:
        return default
    try:
        return expected_type(value)
    except (ValueError, TypeError):
        return default


def first_if_collection(maybe_collection: Union[List[Any], Any]) -> Any:
    return maybe_collection[0] if isinstance(maybe_collection, List) else maybe_collection


def object_size_humanized(any_object: Any) -> Text:
    return _sizeof_fmt(object_size(any_object))


def object_size(any_object: Any) -> int:
    return asizeof(any_object)


def _sizeof_fmt(num: float, suffix: Text = 'B') -> Text:
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)
