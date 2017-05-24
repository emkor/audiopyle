from commons.abstractions.model import Model
from commons.utils.conversion import frames_to_sec


class AudioSegmentMeta(Model):
    def __init__(self, source_file_meta, frame_from, frame_to):
        """
        Represents metadata of a part of an audio wave
        :type source_file_meta: commons.audio.file_meta.AudioFileMeta
        :type frame_from: int
        :type frame_to: int
        """
        self.source_file_meta = source_file_meta
        self.frame_from = frame_from
        self.frame_to = frame_to

    def length_frames(self):
        """
        :rtype: int
        """
        return abs(self.frame_to - self.frame_from)

    def length_sec(self):
        """
        :rtype: float
        """
        return frames_to_sec(self.length_frames(), self.source_file_meta.sample_rate)


class MonoAudioSegment(AudioSegmentMeta):
    def __init__(self, source_file_meta, frame_from, frame_to, data):
        """
        Represents metadata of a part of an audio wave
        :type source_file_meta: commons.audio.file_meta.AudioFileMeta
        :type frame_from: int
        :type frame_to: int
        :type data: numpy.core.multiarray.ndarray
        """
        super(MonoAudioSegment, self).__init__(source_file_meta, frame_from, frame_to)
        self.data = data

    def get_meta(self):
        """
        :rtype: commons.audio.segment.AudioSegmentMeta
        """
        return AudioSegmentMeta(self.source_file_meta, self.frame_from, self.frame_to)

    def __str__(self):
        return super(MonoAudioSegment, self).__str__()
