import wave

from commons.service.file_accessor import FileAccessor
from commons.utils.conversion import B_to_b
from commons.utils.logging_setup import get_logger
from xtracter.model.audio_meta import AudioMeta


class LocalAudioMetaProvider(object):
    def __init__(self, file_provider=FileAccessor):
        self.file_provider = file_provider
        self.logger = get_logger()

    def read_meta_from(self, audio_file_path):
        wave_reader = None
        if self.file_provider.is_file(audio_file_path):
            try:
                filename = self.file_provider.get_file_name(audio_file_path)
                wave_reader = wave.open(audio_file_path, 'rb')
                sample_rate = wave_reader.getframerate()
                channels_count = wave_reader.getnchannels()
                frames_count = wave_reader.getnframes()
                bit_depth = B_to_b(wave_reader.getsampwidth())
                wave_reader.close()
                return AudioMeta(filename, channels_count, sample_rate, frames_count, bit_depth)
            except Exception as e:
                self.logger.error('Error on reading audio meta from file: {}. Details: {}'.format(audio_file_path, e))
                if wave_reader is not None:
                    wave_reader.close()
                return None
        else:
            self.logger.error('Given file does not exist: {}'.format(audio_file_path))
            return None
