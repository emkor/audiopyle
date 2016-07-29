class XtracterConst(object):
    VAMP_PLUGIN_BLACKLIST = ['qm-vamp-plugins:qm-tonalchange', 'nnls-chroma:nnls-chroma',
                             'qm-vamp-plugins:qm-adaptivespectrogram', 'qm-vamp-plugins:qm-chromagram',
                             'qm-vamp-plugins:qm-constantq', 'qm-vamp-plugins:qm-dwt', 'tempogram:tempogram',
                             'vamp-libxtract:dct', 'vamp-libxtract:spectrum', 'vamp-libxtract:peak_spectrum',
                             'cqvamp:cqchromavamp', 'cqvamp:cqvamp', 'cqvamp:cqvampmidi',
                             'vamp-libxtract:harmonic_spectrum']  # mostly visualization plugins
    VAMPY_RAW_FEATURE_VALUES_KEY = 'values'
    VAMPY_RAW_FEATURE_LABEL_KEY = 'label'
    VAMPY_RAW_FEATURE_TIMESTAMP_KEY = 'timestamp'
    TEST_RESOURCES_PATH = "xtracter/xtracter/test/resources"
    TEST_WAV_FILE_NAME = "102bpm_drum_loop_mono_44.1k.wav"
    TEST_MP3_FILE_NAME = "102bpm_drum_loop_mono.mp3"
    TEST_WAV_FILE_FRAME_COUNT = 103936
    TEST_WAV_FILE_CHANNELS_COUNT = 1
    TEST_WAV_FILE_BIT_DEPTH = 16
    TEST_WAV_FILE_SAMPLE_RATE = 44100
    TEST_CSV_FILE_NAME = "102bpm_drum_loop_mono_44.1k.csv"
    DEFAULT_BLOCK_SIZE = 2048
    DEFAULT_STEP_SIZE = 1024  # deprecated
    AUDIO_FILES_CACHE_PATH = "wav_temp"
