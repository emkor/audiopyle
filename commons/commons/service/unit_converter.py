import math


class UnitConverter(object):
    @staticmethod
    def b_to_B(b):
        return math.ceil(b / 8.0)

    @staticmethod
    def B_to_b(B):
        return int(B * 8)

    @staticmethod
    def to_kilo(v):
        return v / 1000.0

    @staticmethod
    def to_mega(v):
        return v / 1000000.0

    @staticmethod
    def frames_to_sec(frames, sample_rate):
        return float(frames) / float(sample_rate)

    @staticmethod
    def sec_to_frames(seconds, sample_rate):
        return int(sample_rate * seconds)

    @staticmethod
    def sec_to_min(sec):
        return float(sec) / float(60)

    @staticmethod
    def min_to_sec(minutes):
        return minutes * 60
