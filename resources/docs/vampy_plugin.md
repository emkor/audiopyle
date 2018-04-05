## VAMP Plugins

### bbc-vamp-plugins:bbc-energy
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Moving average window size (1.0 seconds)
    - Moving average percentile (3.0)
    - Dip threshold (3.0)
    - Low Energy threshold (1.0)
- Outputs:
    - rmsenergy
        - Description: As described above, the term average power refers to the average value of the instantaneous power waveform over time. As this is typically derived from the root mean square (RMS) of the sine wave voltage
        - Summary: Sound energy of all the frequencies at given timestamp
        - Usefulness: 3
    - rmsdelta
        - Description: Difference between RMS of previous and current blocks
        - Comment: Change of sound energy
        - Usefulness: 2
    - lowenergy
        - Description: Percentage of track which is below the low energy threshold
        - Usefulness: 1
    - average
        - Description: Mean of RMS values over moving average window
        - Usefulness: 2
    - pdip
        - Description: Probability of the RMS energy dipping below threshold
        - Usefulness: 1

### bbc-vamp-plugins:bbc-intensity
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Sub-bands (7.0)
    - Window shape (Hann)
- Outputs:
    - intensity
        - Description: Sum of the FFT bin absolute values
        - Comment: Similar to RMS
        - Usefulness: 2
    - intensity-ratio
        - Description: Sum of each sub-bands absolute values
        - Comment: Intensity of each of sub-bands
        - Usefulness: 3

### bbc-vamp-plugins:bbc-peaks
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 256
- Step size:  256
- Parameter (default): None
- Outputs:
    - peaks
        - Description: ?
        - Comment: Wave peaks; almost like original wave
        - Usefulness: 1

### bbc-vamp-plugins:bbc-rhythm
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  256
- Parameter (default):
    - Sub-bands (7)
    - Threshold (1)
    - Moving avg window len (200 frames)
    - Onset peak window length (6 frames)
    - Min BPM 12
    - Max BPM 300
- Outputs:
    - onset_curve
        - Description: Onset detection curve
        - Comment: accent strengths of an rhythm section
        - Usefulness: 3
    - average
        - Description: ?
        - Comment: Moving average of an rhythm accent strengths
        - Usefulness: 3
    - diff
        - Description: Difference between onset and average
        - Comment: Similar to onset_curve, but only highest points are available
        - Usefulness: 1
    - onset
        - Description: ?
        - Comment: Similar to onset_curve, but binary (just points in time)
        - Usefulness: 1
    - avg-onset-freq
        - Description: Rate of onsets per minute
        - Usefulness: 2
    - rhythm-strength
        - Description: Average value of peaks in onset curve
        - Usefulness: 2
    - autocor
        - Description: Autocorrelation of onset detection curve
        - Comment: Does not work?
        - Usefulness: 1
    - mean-correlation-peak
        - Description: Mean of the peak autocorrelation values
        - Comment: Same as above but averaged
        - Usefulness: 1
    - peak-valley-ratio
        - Description: Ratio of the mean correlation peak to the mean correlation valley
        - Usefulness: 1
    - tempo
        - Description: Overall tempo of the track in BPM
        - Usefulness: 2
    
### bbc-vamp-plugins:bbc-spectral-contrast
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  512
- Parameter (default):
    - Alpha (0.02)
    - Sub-bands (7)
- Outputs:
    - valleys
        - Description: Valley of the spectrum
        - Comment: Values per sub-band, similar to intensity but less reasonable
        - Usefulness: 2
    - peaks
        - Description: Peak of the spectrum
        - Comment: Spectrum peaks per sub-band, more reasonable than valleys
        - Usefulness: 3
    - mean
        - Description: Mean of the spectrum
        - Comment: Average spectrum per sub-band (bass bands have higher values)
        - Usefulness: 2

### bbc-vamp-plugins:bbc-spectral-flux
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Use L2 norm over L1 (False)
- Outputs:
    - spectral-flux
        - Description: ?
        - Comment: Similar to RMS / Intensity but averaged(?)
        - Usefulness: 2
    
### bbc-vamp-plugins:bbc-speechmusic-segmenter
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Resolution (256)
    - Change threshold (0.08)
    - Decision threshold (0.27)
    - Minimum music segment length (0.0)
    - Margin (14.0)
- Outputs:
    - segmentation
        - Description: Segmentation
        - Comment: Splits music and spoken word (binary segments)
        - Usefulness: 1
    - skewness
        - Description: Detection function
        - Comment: Probability of spoken word
        - Usefulness: 2

### beatroot-vamp:beatroot
- URL:        https://code.soundsoftware.ac.uk/projects/beatroot-vamp
- Block size: 2048
- Step size:  441
- Parameter (default):
    - Pre-Margin factor (0.15)
    - Post-Margin factor (0.3)
    - Maximum Change (0.2)
    - Expiry Time (10.0)
- Outputs:
    - beats
        - Description: Identify beat locations in music
        - Comment: Binary points for beat locations
        - Usefulness: 2

### cqvamp:cqchromavamp
- URL:        https://github.com/cannam/constant-q-cpp
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Lowest Contributing Octave (0)
    - Contributing Octave Count (7)
    - Tuning Frequency (440 Hz)
    - Bins per Octave (36)
- Outputs:
    - chromagram
        - Description: Extract Constant-Q spectrogram with a constant ratio of centre frequency to resolution from the audio, then wrap it around into a single-octave chromagram
        - Comment: Intensity of a sound on particular note (notes range: 0-35; 1 - C, 4 - C#, 7 - D, …, 34 - B)
        - Usefulness: 3

### cqvamp:cqvamp
- URL:        https://github.com/cannam/constant-q-cpp
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Minimum Frequency (110 Hz)
    - Maximum Frequency (14700 Hz)
    - Bins per Octave (36 bins)
    - Interpolation (Linear)
- Outputs:
    - constantq
        - Description: Extract a spectrogram with constant ratio of centre frequency to resolution from the input audio, specifying the frequency range in Hz
        - Comment: Intensity of a sound in particular frequency range (288 separate ranges)
        - Usefulness: 1

### cqvamp:cqvampmidi
- URL:        https://github.com/cannam/constant-q-cpp
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Minimum Pitch (36 MIDI units)
    - Maximum Pitch (96 MID units)
    - Tuning Frequency (440 Hz)
    - Bins per Octave (36)
    - Interpolation (Linear)
- Outputs:
    - constantq
        - Description: Extract spectrogram with constant ratio of centre frequency to resolution from the input audio, specifying the frequency range in MIDI pitch units
        - Comment: Intensity of a sound on particular note (180 zakresów; 0 - C#2, 1 - D2, …, 180 - C7)
        - Usefulness: 3

### match-vamp-plugin-2:match
- URL: https://code.soundsoftware.ac.uk/projects/match-vamp
- Outputs:
    - path
    - a_b
    - b_a
    - a_b_divergence
    - a_b_temporatio
    - a_features
    - b_features
    - a_cfeatures
    - b_cfeatures
    - overall_cost

### match-vamp-plugin:match
- URL: https://code.soundsoftware.ac.uk/projects/match-vamp
- Outputs:
    - path
    - a_b
    - b_a
    - a_b_divergence
    - a_b_temporatio
    - a_features
    - b_features
    - a_cfeatures
    - b_cfeatures
    - overall_cost

### mtg-melodia:melodia
- URL:        https://www.upf.edu/web/mtg/melodia
- Block size: 2048
- Step size:  128
- Parameter (default):
    - Program (Polyphonic)
    - Min Freq: 55 Hz
    - Max Freq: 1760 Hz
    - Voicing Tolerance: 0.2
    - Monophonic Noise Filter: 0
- Outputs:
    - melody
    
### mtg-melodia:melodiaviz
- URL:    https://www.upf.edu/web/mtg/melodia
- Outputs:
    - saliencefunction
    - contoursall
    - contoursmelody

### nnls-chroma:chordino
- URL: http://www.isophonics.net/nnls-chroma
- Block size: 16384
- Step size:  2048
- Parameter (default):
    - Use approximate transcription (NNLS)
    - Bass noise threshold (0.0 %)
    - Tuning mode (global tuning)
    - Spectral whitening (1.0)
    - Spectral shape (0.7)
    - Boost N (0.1)
- Outputs:
    - simplechord
    - chordnotes
    - harmonicchange
    - loglikelihood

### nnls-chroma:nnls-chroma
- URL: http://www.isophonics.net/nnls-chroma
- Block size: 16384
- Step size:  2048
- Parameter (default):
    - Use approximate transcription (NNLS)
    - Bass noise threshold (0.0 %)
    - Tuning mode (global tuning)
    - Spectral whitening (1.0)
    - Spectral shape (0.7)
    - Chroma normalization (None)
- Outputs:
    - logfreqspec
    - tunedlogfreqspec
    - semitonespectrum
    - chroma
    - basschroma
    - bothchroma

### nnls-chroma:tuning
- URL: http://www.isophonics.net/nnls-chroma
- Block size: 16384
- Step size:  8192
- Parameter (default):
    - Bass noise threshold (0.0%)
- Outputs:
    - tuning
    - localtuning
    
### pyin:localcandidatepyin
- URL: https://code.soundsoftware.ac.uk/projects/pyin
- Block size: 2048
- Step size:  256
- Parameter (default):
    - Yin threshold distribution (Beta)
    - Output estimates classified as unvoiced? (No)
    - Use non-standard precise YIN timing (slow) (False)
- Outputs:
    - pitchtrackcandidates

### pyin:pyin
- URL: https://code.soundsoftware.ac.uk/projects/pyin
- Block size: 2048
- Step size:  256
- Parameter (default):
    - Yin threshold distribution (Beta)
    - Output estimates classified as unvoiced? (No)
    - Use non-standard precise YIN timing (slow) (False)
    - Suppress low amplitude pitch estimates (0.1)
    - Onset sensitivity (0.7)
    - Duration pruning threshold (0.1)
- Outputs:
    - f0candidates
    - f0probs
    - voicedprob
    - candidatesalience
    - smoothedpitchtrack
    - notes

### pyin:yin
- Outputs:
    - f0
    - periodicity
    - rms
    - salience

### qm-vamp-plugins:qm-adaptivespectrogram
- URL: https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Number of resolutions (3)
    - Smallest resolution (512)
    - Decimation factor (No decimation)
    - Omit alternate solutions (False)
    - Multi-threaded processing (True)
- Outputs:
    - output

### qm-vamp-plugins:qm-barbeattracker
- URL: https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 1024
- Step size:  512
- Parameter (default):
    - Beats per bar (4)
    - Alpha (0.9)
    - Tempo hint (120 BPM)
    - Constrain Tempo (False)
- Outputs:
    - beats
    - bars
    - beatcounts
    - beatsd

### qm-vamp-plugins:qm-chromagram
- Outputs:
    - chromagram
    - chromameans

### qm-vamp-plugins:qm-constantq
- Outputs:
    - constantq

### qm-vamp-plugins:qm-dwt
- Outputs:
    - wcoeff

### qm-vamp-plugins:qm-keydetector
- Outputs:
    - tonic
    - mode
    - key
    - keystrength

### qm-vamp-plugins:qm-mfcc
- Outputs:
    - coefficients
    - means

### qm-vamp-plugins:qm-onsetdetector
- Outputs:
    - onsets
    - detection_fn
    - smoothed_df

### qm-vamp-plugins:qm-segmenter
- Outputs:
    - segmentation

### qm-vamp-plugins:qm-similarity
- Outputs:
    - distancematrix
    - distancevector
    - sorteddistancevector
    - means
    - variances
    - beatspectrum

### qm-vamp-plugins:qm-tempotracker
- Outputs:
    - beats
    - detection_fn
    - tempo


### qm-vamp-plugins:qm-tonalchange
- Outputs:
    - tcstransform
    - tcfunction
    - changepositions

### qm-vamp-plugins:qm-transcription
- Outputs:
    - transcription

### segmentino:segmentino
- Outputs:
    - segmentation

### silvet:silvet
- Outputs:
    - notes
    - onsets
    - onoffsets
    - timefreq
    - pitchactivation
    - chroma
    - templates

### tempogram:tempogram
- Outputs:
    - cyclicTempogram
    - tempogramDFT
    - tempogramACT
    - nc

### ua-vamp-plugins
- Outputs:
    - mf0ua
    - onsetsua
    - onsetsua

### vamp-example-plugins:amplitudefollower
- Outputs:
    - amplitude

### vamp-example-plugins:fixedtempo
- Outputs:
    - tempo
    - candidates
    - detectionfunction
    - acf
    - filtered_acf

### vamp-example-plugins:percussiononsets
- Outputs:
    - onsets
    - detectionfunction

### vamp-example-plugins:powerspectrum
- Outputs:
    - powerspectrum

### vamp-example-plugins:spectralcentroid
- Outputs:
    - logcentroid
    - linearcentroid

### vamp-example-plugins:zerocrossing
- Outputs:
    - counts
    - zerocrossings

### vamp-libxtract:amdf
- Outputs:
    - amdf
    - asdf

### vamp-libxtract:autocorrelation
- Outputs:
    - autocorrelation

### vamp-libxtract:average_deviation
- Outputs:
    - average_deviation

### vamp-libxtract:bark_coefficients
- Outputs:
    - bark_coefficients

### vamp-libxtract:crest
- Outputs:
    - crest

### vamp-libxtract:dct
- Outputs:
    - dct

### vamp-libxtract:f0
- Outputs:
    - f0

### vamp-libxtract:failsafe_f0
- Outputs:
    - failsafe_f0

### vamp-libxtract:flatness
- Outputs:
    - flatness

### vamp-libxtract:harmonic_spectrum
- Outputs:
    - amplitudes

### vamp-libxtract:highest_value
- Outputs:
    - highest_value

### vamp-libxtract:irregularity_j
- Outputs:
    - irregularity_j

### vamp-libxtract:irregularity_k
- Outputs:
    - irregularity_k

### vamp-libxtract:kurtosis
- Outputs:
    - kurtosis

### vamp-libxtract:loudness
- Outputs:
    - loudness

### vamp-libxtract:lowest_value
- Outputs:
    - lowest_value

### vamp-libxtract:mean
- Outputs:
    - mean

### vamp-libxtract:mfcc
- Outputs:
    - mfcc

### vamp-libxtract:noisiness
- Outputs:
    - noisiness

### vamp-libxtract:nonzero_count
- Outputs:
    - nonzero_count

### vamp-libxtract:odd_even_ratio
- Outputs:
    - odd_even_ratio

### vamp-libxtract:peak_spectrum
- Outputs:
    - amplitudes

### vamp-libxtract:rms_amplitude
- Outputs:
    - rms_amplitude

### vamp-libxtract:rolloff
- Outputs:
    - rolloff

### vamp-libxtract:sharpness
- Outputs:
    - sharpness

### vamp-libxtract:skewness
- Outputs:
    - skewness

### vamp-libxtract:smoothness
- Outputs:
    - smoothness

### vamp-libxtract:spectral_centroid
- Outputs:
    - spectral_centroid

### vamp-libxtract:spectral_inharmonicity
- Outputs:
    - spectral_inharmonicity

### vamp-libxtract:spectral_kurtosis
- Outputs:
    - spectral_kurtosis

### vamp-libxtract:spectral_skewness
- Outputs:
    - spectral_skewness

### vamp-libxtract:spectral_slope
- Outputs:
    - spectral_slope

### vamp-libxtract:spectral_standard_deviation
- Outputs:
    - spectral_standard_deviation

### vamp-libxtract:spectral_variance
- Outputs:
    - spectral_variance

### vamp-libxtract:spectrum
- Outputs:
    - amplitudes

### vamp-libxtract:spread
- Outputs:
    - spread

### vamp-libxtract:standard_deviation
- Outputs:
    - standard_deviation

### vamp-libxtract:sum
- Outputs:
    - sum

### vamp-libxtract:tonality
- Outputs:
    - tonality

### vamp-libxtract:tristimulus_1
- Outputs:
    - tristimulus_1

### vamp-libxtract:tristimulus_2
- Outputs:
    - tristimulus_2

### vamp-libxtract:tristimulus_3
- Outputs:
    - tristimulus_3

### vamp-libxtract:variance
- Outputs:
    - variance

### vamp-libxtract:zcr
- Outputs:
    - zcr
