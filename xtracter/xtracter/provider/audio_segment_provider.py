import struct
import wave

import numpy
from numpy import array

from commons.model.audio_segment import AudioSegment
from commons.service.file_accessor import FileAccessor


class LocalAudioSegmentProvider(object):
    def __init__(self, audio_files_path, wav_lib=wave):
        self.audio_files_path = audio_files_path
        self.wav_lib = wav_lib

    def read_segment(self, audio_meta, start_frame=0, end_on_frame=None, return_left_if_stereo=True):
        if not end_on_frame or end_on_frame > audio_meta.frames_count:
            end_on_frame = audio_meta.frames_count
        audio_file_path = FileAccessor.join(self.audio_files_path, audio_meta.filename)
        read_frames = self._read_audio_from_file(audio_file_path, audio_meta, end_on_frame)
        l_channel, r_channel = self._split_by_channels(read_frames, audio_meta.channels_count)
        l_channel, r_channel = self._cut(l_channel, start_frame), self._cut(r_channel, start_frame)
        l_channel, r_channel = self._normalize(l_channel), self._normalize(r_channel)
        if return_left_if_stereo:
            return AudioSegment(l_channel, audio_meta.sample_rate, start_frame)
        else:
            # TODO implement downmixing to mono
            raise NotImplementedError("implement downmixing to mono")

    def _read_audio_from_file(self, file_path, audio_meta, end_on_frame):
        wav_file = None
        try:
            wav_file = self.wav_lib.open(file_path, "r")
            read_frames = wav_file.readframes(end_on_frame * audio_meta.channels_count)
            wav_file.close()
            return struct.unpack_from("%dh" % end_on_frame * audio_meta.channels_count, read_frames)
        except Exception as e:
            print(
                'Error on reading audio from: {} with meta: {}. Details: {}'.format(file_path, audio_meta,
                                                                                    e))
            if wav_file:
                wav_file.close()

    def _split_by_channels(self, read_frames, channels_count):
        if channels_count == 2:
            left = array(list(read_frames[0::2]))
            right = array(list(read_frames[1::2]))
            return left, right
        else:
            return read_frames, None

    def _normalize(self, int_channel):
        return numpy.asarray(
                [signal_value / 32767.0 for signal_value in int_channel]) if int_channel is not None else None

    def _cut(self, mono_channel, start_frame):
        return mono_channel[start_frame:] if mono_channel else None
