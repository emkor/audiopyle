#!/bin/python3

from mutagen.flac import FLAC


def main(flac_file_path):
    audio = FLAC(flac_file_path)
    audio.delete()
    audio.save()

    audio = FLAC(flac_file_path)
    audio["title"] = "Unknown Title"
    audio["artist"] = "Unknown Artist"
    audio["album"] = "Unknown Album"
    audio["date"] = "2017"
    audio["genre"] = "Unknown Genre"
    audio["tracknumber"] = "1"
    audio.save()


if __name__ == "__main__":
    main("/home/mat/projects/audiopyle/resources/audio/102bpm_drum_loop.flac")
