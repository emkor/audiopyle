import logging
from pydub import AudioSegment

from commons.service.file_accessor import FileAccessor

DEFAULT_TARGET_CHANNEL_NUMBER = 1
DEFAULT_TARGET_SAMPLE_RATE = 44100
DEFAULT_TARGET_SAMPLE_WIDTH = 2

logging.basicConfig(format='%(asctime)s %(levelname)s:%(funcName)s %(message)s', level=logging.INFO)


class AudioFileConverter(object):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def convert(self, input_file):
        output_file = input_file + ".wav"

        full_input_path = FileAccessor.join(self.input_dir, input_file)
        full_output_path = FileAccessor.join(self.output_dir, output_file)

        song = AudioSegment.from_mp3(full_input_path)\
            .set_channels(DEFAULT_TARGET_CHANNEL_NUMBER)\
            .set_frame_rate(DEFAULT_TARGET_SAMPLE_RATE)\
            .set_sample_width(DEFAULT_TARGET_SAMPLE_WIDTH)

        try:
            song.export(full_output_path, format="wav")
        except Exception as ex:
            logging.error("Some problems on conversion file: {}".format(input_file))
            logging.error("Details: {}".format(ex))
