from pydub import AudioSegment

from commons.service.file_accessor import FileAccessor

DEFAULT_TARGET_CHANNEL_NUMBER = 1
DEFAULT_TARGET_SAMPLE_RATE = 44100
DEFAULT_TARGET_SAMPLE_WIDTH = 2


class AudioFileConverter(object):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def convert(self, input_file):
        self.input_file = input_file
        self.output_file = self.input_file + ".wav"

        self.full_input_path = FileAccessor.join(
            self.input_dir, self.input_file)

        self.full_output_path = FileAccessor.join(
            self.output_dir, self.output_file)

        self.song = AudioSegment.from_mp3(self.full_input_path)

        self.song_mono = self.song.set_channels(DEFAULT_TARGET_CHANNEL_NUMBER)

        self.song_sample_rate = self.song_mono.set_frame_rate(
            DEFAULT_TARGET_SAMPLE_RATE)

        self.song_sample_width = self.song_sample_rate.set_sample_width(
            DEFAULT_TARGET_SAMPLE_WIDTH)

        self.song_sample_width.export(self.full_output_path, format="wav")
