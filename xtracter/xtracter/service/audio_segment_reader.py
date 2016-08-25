import numpy

from xtracter.utils.xtracter_const import DEFAULT_BLOCK_SIZE


class AudioSegmentReader(object):
    def __init__(self, segment_provider):
        self.provider = segment_provider

    def read_segments(self, audio_meta, block_size=DEFAULT_BLOCK_SIZE):
        current_frame = 0
        if not block_size:
            block_size = audio_meta.frames_count
        segments = []
        while current_frame < audio_meta.frames_count:
            audio_segment = self.provider.read_segment(audio_meta, current_frame, current_frame + block_size)
            current_frame = audio_segment.next_offset()
            audio_segment = self._resize_and_fill_with(audio_segment, block_size)
            segments.append(audio_segment)
        return segments

    def _resize_and_fill_with(self, audio_segment, block_size, fill=0.0):
        if audio_segment.length_frames() < block_size:
            missing = block_size - audio_segment.length_frames()
            audio_segment.data = numpy.append(audio_segment.data, [fill] * missing)
            audio_segment.length = block_size
        return audio_segment
