import sys
from pydub import AudioSegment

input_dir = "./"
output_dir = "./"

input_file = sys.argv[1]
output_file = input_file + ".wav"

full_input_path = input_dir + input_file
full_output_path = output_dir + output_file

song = AudioSegment.from_mp3(full_input_path)
song_mono = song.set_channels(1).set_frame_rate(44100).set_sample_width(2)
song_mono.export(full_output_path, format="wav")
