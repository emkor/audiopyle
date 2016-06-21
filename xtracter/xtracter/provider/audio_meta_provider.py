import logging
import wave

from commons.service.file_accessor import FileAccessor
from commons.service.unit_converter import UnitConverter
from xtracter.model.audio_meta import AudioMeta


class LocalAudioMetaProvider(object):
    def __init__(self, file_provider=FileAccessor, unit_converter=UnitConverter):
        self.file_provider = file_provider
        self.unit_converter = unit_converter

    def read_meta_from(self, audio_file_path):
        wave_reader = None
        if self.file_provider.is_file(audio_file_path):
            try:
                filename = self.file_provider.get_file_name(audio_file_path)
                wave_reader = wave.open(audio_file_path, 'rb')
                sample_rate = wave_reader.getframerate()
                channels_count = wave_reader.getnchannels()
                frames_count = wave_reader.getnframes()
                bit_depth = self.unit_converter.B_to_b(wave_reader.getsampwidth())
                wave_reader.close()
                return AudioMeta(filename, channels_count, sample_rate, frames_count, bit_depth)
            except Exception as e:
                logging.error('Error on reading audio meta from file: {}. Details: {}'.format(audio_file_path, e))
                if wave_reader is not None:
                    wave_reader.close()
                return None
        else:
            logging.error('Given file does not exist: {}'.format(audio_file_path))
            return None