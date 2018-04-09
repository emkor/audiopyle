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
        - Comment: Intensity of a sound on particular note (180 notes; 0 - C#2, 1 - D2, …, 180 - C7)
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
        - Description: Estimates the melody pitch in polyphonic music; segments without melody are indicated by zero or negative values
        - Comment: ? Very weird chart
        - Usefulness: 1
    
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
        - Description: Chord Estimate: Estimated chord times and labels
        - Comment: Segments of chords (just labels without values)
        - Usefulness: 2
    - chordnotes
        - Description: Note representation of Chord Estimate
        - Comment: Estimates of notes in the chord
        - Usefulness: 2
    - harmonicchange
        - Description: An indication of the likelihood of harmonic change
        - Comment: Probability of chord change
        - Usefulness: 2
    - loglikelihood
        - Description: Logarithm of the likelihood value of the simple chord estimate
        - Comment: As harmonicchange, but less reasonable
        - Usefulness: 1

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
        - Description: Log-Frequency Spectrum (constant Q) that is obtained by cosine filter mapping
        - Comment: As tunedlogfreqspec, but more blurry
        - Usefulness: 0
    - tunedlogfreqspec
        - Description: Log-Frequency Spectrum (constant Q) that is obtained by cosine filter mapping, then its tuned using the estimated tuning frequency
        - Comment: Very precise map of sound intensity with lot of gaps between single notes; no labels; values range: 0-256(?)
        - Usefulness: 1
    - semitonespectrum
        - Description: A semitone-spaced log-frequency spectrum derived from the third-of-a-semitone-spaced tuned log-frequency spectrum
        - Comment: Semitone estimate (values 0-84, no labels)
        - Usefulness: 1
    - chroma
        - Description: Tuning-adjusted chromagram from NNLS approximate transcription, with an emphasis on the medium note range
        - Comment: Estimate of note intensity (values 0-12; 0 - A, 1 - Bb, …, 12 - Ab) with emphasis on mid-band
        - Usefulness: 3
    - basschroma
        - Description: Tuning-adjusted bass chromagram from NNLS approximate transcription, with an emphasis on the bass note range
        - Comment: Estimate of note intensity (values 0-12; 0 - A, 1 - Bb, …, 12 - Ab) with emphasis on bass-band
        - Usefulness: 3
    - bothchroma
        - Description: Tuning-adjusted chromagram from NNLS approximate transcription, with an emphasis on the medium note range
        - Comment: Estimate of note intensity (values 0-24;  0 - A bass, 1 - Bb bass, …, 13 - A, …, 24 - Ab)
        - Usefulness: 2

### nnls-chroma:tuning
- URL: http://www.isophonics.net/nnls-chroma
- Block size: 16384
- Step size:  8192
- Parameter (default):
    - Bass noise threshold (0.0%)
- Outputs:
    - tuning
        - Description: Returns singe-label containing estimated concert pitch tuning in Hz
        - Comment: ?
        - Usefulness: 0
    - localtuning
        - Description: Returns per-analysis-frame tuning estimate
        - Comment: Tuning estimate in each point (would be nice for large block size?)
        - Usefulness: 2
    
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
        - Description: Monophonic pitch and note tracking based on probabilistic Yin extension
        - Comment: ? Did not finish
        - Usefulness: 0

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
        - Description: Estimated fundamental frequency candidates
        - Comment: Estimated frequency at point (Hz)
        - Usefulness: 1
    - f0probs
        - Description: Probability of estimated fundamental frequency candidates
        - Comment: Probability of f0candidates
        - Usefulness: 0
    - voicedprob
        - Description: Probability that signal is voiced according to Probabilistic Yin
        - Comment: ? Seems unreasonable
        - Usefulness: 1
    - candidatesalience
        - Description: Candidate salience
        - Comment: ? Seems unreasonable
        - Usefulness: 1
    - smoothedpitchtrack
        - Description: ?
        - Comment: ?
        - Usefulness: 1
    - notes
        - Description: Derived fixed-pitch note frequencies
        - Comment: Notes estimate; pointless
        - Usefulness: 0

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
        - Description: Adaptive Spectrogram produces a composite spectrogram from a set of series of short-time Fourier transforms at differing resolutions. Values are selected from these spectrograms by repeated subdivision by time and frequency in order to maximise an entropy function across each column
        - Comment: Notes mixed with percussion?
        - Usefulness: 1

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
        - Description: The estimated beat locations, returned as a single feature, with timestamp but no value, for each beat, labelled with the number of that beat within the bar (e.g. consecutively 1, 2, 3, 4 for 4 beats to the bar)
        - Comment: Detects beats in bars, labels are beat count in a bar
        - Usefulness: 3
    - bars
        - Description: The estimated bar line locations, returned as a single feature, with timestamp but no value, for each bar
        - Comment: Detects bars
        - Usefulness: 2
    - beatcounts
        - Description: The estimated beat locations, returned as a single feature, with timestamp and a value corresponding to the number of that beat within the bar. This is similar to the Beats output except that it returns a counting function rather than a series of instants
        - Comment: Counts beats in bar
        - Usefulness: 0
    - beatsd
        - Description: The new-bar likelihood function used in bar line estimation
        - Comment: Likelihood of new bar 
        - Usefulness: 1

### qm-vamp-plugins:qm-chromagram
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 16384
- Step size:  2048
- Parameter (default):
    - Minimum Pitch (36 MIDI units)
    - Maximum Pitch (96 MIDI units)
    - Tuning Frequency (440 Hz)
    - Bins per Octave (12 bins)
    - Normalization (None)
- Outputs:
    - chromagram
        - Description: Output of a chromagram, as a single vector per process block
        - Comment: Note detection in given point (0-12 values; 0-C, 12-B)
        - Usefulness: 3
    - chromameans
        - Description: Mean values of chromagram bins across duration of the input audio
        - Comment: Some kind of averaged notes from overall track?
        - Usefulness: 3

### qm-vamp-plugins:qm-constantq
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 16384
- Step size:  2048
- Parameter (default):
    - Minimum Pitch (36 MIDI units)
    - Maximum Pitch (84 MIDI units)
    - Tuning Frequency (440 Hz)
    - Bins per Octave (12 bins)
    - Normalization (False)
- Outputs:
    - constantq
        - Description: Extract a spectrogram with constant ratio of centre frequency to resolution from the input audio
        - Comment: Sound energy on given note (across octaves)
        - Usefulness: 2

### qm-vamp-plugins:qm-dwt
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Scales (10)
    - Wavelet (Haar)
    - Threshold (0.0)
    - Absolute values (False)
- Outputs:
    - wcoeff
        - Description: (Discrete Wavelet Transform) Visualization by scalogram
        - Comment: ?
        - Usefulness: 1? 

### qm-vamp-plugins:qm-keydetector
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 32768
- Step size:  32768
- Parameter (default):
    - Tuning Frequency (440 Hz)
    - Window Length (10 chroma frames)
- Outputs:
    - tonic
        - Description: Tonic of the estimated key (from C=1 to B=12)
        - Comment: Segments of keys (F#, Ab etc)
        - Usefulness: 2
    - mode
        - Description: Estimates the key of music; major or minor mode of the estimated key (major = 0, minor = 1)
        - Comment: Binary segments; either minor or major; can be combined with notes! 
        - Usefulness: 2
    - key
        - Description: Estimated key (from C major = 1 to B major = 12 and C minor = 13 to B minor = 24)
        - Comment: Combination of mode and tonic; seems very useful!
        - Usefulness: 3
    - keystrength
        - Description: Correlation of the chroma vector with stored key profile for each major and minor key
        - Comment: value of 13 is empty; 1-12 is major, 14-25 is minor; seems weird but may be useful
        - Usefulness: 2

### qm-vamp-plugins:qm-mfcc
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 2048
- Step size:  1024
- Parameter (default):
    - Number of Coefficients (20)
    - Power of Mel Amplitude Logs (1)
    - Include C0 (True)
- Outputs:
    - coefficients
        - Description: MFCC Values
        - Comment: ?
        - Usefulness: 1 
    - means
        - Description: Mean values of MFCCs across duration of audio input
        - Comment: ?
        - Usefulness: Same as above but single values for each MFCC

### qm-vamp-plugins:qm-onsetdetector
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 1024
- Step size:  512
- Parameter (default):
    - Program (None, General purpose, Soft onsets, Percussive onsets)
    - Onset Detection Function Type (Complex Domain)
    - Onset Detector Sensitivity (50%)
    - Adaptive Whitening (False)
- Outputs:
    - onsets
        - Description: Perceived note onset positions
        - Comment: Binary points indicating note/percussion etc.
        - Usefulness: 0
    - detection_fn
        - Description: Probability function of note onset likelihood
        - Comment: As onsets but with probability per point
        - Usefulness: 1
    - smoothed_df
        - Description: Smoothed probability function used for peak-picking
        - Comment: As detection_fn but smoothed
        - Usefulness: 2

### qm-vamp-plugins:qm-segmenter
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 28800
- Step size:  9600
- Parameter (default):
    - Number of segment-types (10)
    - Feature Type (Hybrid (Constant-Q))
    - Minimum segment duration (4)
- Outputs:
    - segmentation
        - Description: Divide the tack into a sequence of consistent segments
        - Comment: Shows repeatable segments of a song
        - Usefulness: 3

### qm-vamp-plugins:qm-similarity
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 4096
- Step size:  2048
- Parameter (default):
    - Feature Type (Timbre and Rhythm; Timbre; Chroma; Chroma and Rhythm; Rhythm)
- Outputs:
    - distancematrix
        - Description: Distance matrix for similarity metric. Smaller = more similar. Should be assymetrical.
        - Comment: 4 values, 2 per channel
        - Usefulness: 1?
    - distancevector (Distance from first channel)
        - Description: Distance vector for similarity of each channel to the first channel. Smaller = more similar.
        - Comment: Two values (one per channel)
        - Usefulness: 1
    - sorteddistancevector
        - Description: 
        - Comment: ? 
        - Usefulness: ?
    - means
        - Description: Means of the feature bins. Feature time (sec) corresponds to input channel. Number of bins depends on selected feature type.
        - Comment: ?
        - Usefulness: ?
    - variances
        - Description: Variances of the feature bins. Feature time (sec) corresponds to input channel. Number of bins depends on selected feature type.
        - Comment: ?
        - Usefulness: ? 
    - beatspectrum
        - Description: Rhythmic self-similarity vectors (beat spectra) for the input channels. Feature time (sec) corresponds to input channel. Not returned if rhythm weighting is zero.
        - Comment: ?
        - Usefulness: ?

### qm-vamp-plugins:qm-tempotracker
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 1114
- Step size:  557
- Parameter (default):
    - Beat Tracking Method (New)
    - Onset detection function type (Complex Domain)
    - Adaptive Whitening (False)
    - Alpha (0.9)
    - Tempo Hint (120 BPM)
    - Constrain Tempo (False)
- Outputs:
    - beats
        - Description: Estimated metrical beat locations
        - Comment: HANGS
        - Usefulness: ?
    - detection_fn
        - Description: Probability function of note onset likelihood
        - Comment: HANGS
        - Usefulness: ?
    - tempo
        - Description: Locked tempo estimates
        - Comment: HANGS
        - Usefulness: ?


### qm-vamp-plugins:qm-tonalchange
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 16384
- Step size:  2048
- Parameter (default):
    - Gaussian smoothing (5 frames)
    - Chromagram minimum pitch (32 MIDI units)
    - Chromagram maximum pitch (108 MIDI units)
    - Chromagram tuning frequency 440 Hz)
- Outputs:
    - tcstransform (Transform to 6D Tonal Content Space)
        - Description: Representation of content in a six-dimensional tonal space
        - Comment: ?
        - Usefulness: 1? 
    - tcfunction (Tonal Change Detection Function)
        - Description: Estimate of the likelihood of a tonal change occurring within each spectral frame
        - Comment: ? Flat line
        - Usefulness: 2?
    - changepositions (Tonal Change Positions)
        - Description: Estimated locations of tonal changes
        - Comment: ?
        - Usefulness: 1? 

### qm-vamp-plugins:qm-transcription
- URL:        https://vamp-plugins.org/plugin-doc/qm-vamp-plugins.html
- Block size: 441
- Step size:  441
- Parameter (default):
    - (None)
- Outputs:
    - transcription (Polyphonic Transcritpion)
        - Description: Transcribe the input audio to estimated notes
        - Comment: Shows MIDI notes in time
        - Usefulness: 1

### segmentino:segmentino
- URL:        https://code.soundsoftware.ac.uk/projects/segmenter-vamp-plugin
- Block size: 32768
- Step size:  557
- Parameter (default):
    - (None)
- Outputs:
    - segmentation
        - Description: Estimates contiguous segents pertaining to song parts such as verse and chorus
        - Comment: Shows segments of a song
        - Usefulness: 3

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
