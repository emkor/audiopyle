## Glossary

- Audio tag - ID3 tag embedded in audio files (MP3, FLAC etc.; WAV does not support ID3 tags) containing info like artist name, song title, genre etc.; details: https://en.wikipedia.org/wiki/ID3
- Audio meta - audio stream metadata; contains information on sample rate, bit depth, frames count, file size etc.; when it comes to MP3 file, contains also bitrate (kb/s)
- Sample rate - number of frames per second; see [Sampling](https://en.wikipedia.org/wiki/Sampling_(signal_processing))
- Audio frame - single point of audio-level measurement in time-domain

- VAMP plugin - system library that does direct feature extraction; see [Vamp plugins page](https://vamp-plugins.org/)
- Bit depth - number of bits for storing audio-wave level; standard: 16 bit; see [Audio bit depth](https://en.wikipedia.org/wiki/Audio_bit_depth)
- Audio feature - raw feature from VAMP plugin output, wrapped in audiopyle-specific class abstraction
- Variable step feature - one of two feature types from VAMP plugin output; basically, list of dictionaries, each one with timestamp, value and label (optionally)
- Constant step feature - second feature type; dictionary containing feature_step value (seconds between subsequent measures) and vector or matrix of measured values
- Block size / window size - size of a block (in frames count) analyzed in single step by VAMP plugin
- Block size increment / window increment - frames count by which block size is incremented between steps