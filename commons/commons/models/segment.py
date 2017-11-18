from typing import Any, Text, Dict

from numpy.core.multiarray import ndarray

from commons.abstractions.model import Model
from commons.models.file_meta import AudioFileMeta, WavAudioFileMeta
from commons.utils.conversion import frames_to_sec


class AudioSegmentMeta(Model):
    def __init__(self, source_file_meta: AudioFileMeta, frame_from: int, frame_to: int) -> None:
        """Represents metadata of a part of an audio wave"""
        self.source_file_meta = source_file_meta
        self.frame_from = frame_from
        self.frame_to = frame_to

    def length_frames(self) -> int:
        return abs(self.frame_to - self.frame_from + 1)

    def length_sec(self) -> float:
        return frames_to_sec(self.length_frames(), self.source_file_meta.sample_rate)

    def serialize(self):
        super_serialized = super(AudioSegmentMeta, self).serialize()
        super_serialized.update({"source_file_meta": self.source_file_meta.serialize()})
        return super_serialized

    @classmethod
    def deserialize(cls, serialized: Dict[Text, Any]):
        source_file_meta = WavAudioFileMeta.deserialize(serialized.pop("source_file_meta"))
        serialized.update({"source_file_meta": source_file_meta})
        return AudioSegmentMeta(**serialized)


class MonoAudioSegment(AudioSegmentMeta):
    def __init__(self, source_file_meta: AudioFileMeta, frame_from: int, frame_to: int, data: ndarray) -> None:
        super(MonoAudioSegment, self).__init__(source_file_meta, frame_from, frame_to)
        self.data = data

    def get_meta(self) -> AudioSegmentMeta:
        return AudioSegmentMeta(self.source_file_meta, self.frame_from, self.frame_to)

    def __str__(self):
        return super(MonoAudioSegment, self).__str__()

    def serialize(self):
        super_serialized = super(MonoAudioSegment, self).serialize()
        super_serialized.update({"data": self.data.tolist()})
        return super_serialized
