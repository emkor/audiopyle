from pydub import AudioSegment


class AudioFileConverter(object):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def convert(self, input_file):
        self.input_file = input_file
        self.output_file = self.input_file + ".wav"
        self.full_input_path = self.input_dir + self.input_file
        self.full_output_path = self.output_dir + self.output_file

        self.song = AudioSegment.from_mp3(self.full_input_path)
        self.song_mono = self.song.set_channels(1)
        self.song_44100 = self.song_mono.set_frame_rate(44100)
        self.song_sample_width = self.song_44100.set_sample_width(2)
        self.song_sample_width.export(self.full_output_path, format="wav")
