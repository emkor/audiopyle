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
    - rmsdelta
    - lowenergy
    - average
    - pdip

### bbc-vamp-plugins:bbc-intensity
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Sub-bands (7.0)
    - Window shape (Hann)
- Outputs:
    - intensity
    - intensity-ratio

### bbc-vamp-plugins:bbc-peaks
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 256
- Step size:  256
- Parameter (default): None
- Outputs:
    - peaks

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
    - average
    - diff
    - onset
    - avg-onset-freq
    - rhythm-strength
    - autocor
    - mean-correlation-peak
    - peak-valley-ratio
    - autocor
    - tempo
    
### bbc-vamp-plugins:bbc-spectral-contrast
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  512
- Parameter (default):
    - Alpha (0.02)
    - Sub-bands (7)
- Outputs:
    - valleys
    - peaks
    - mean

### bbc-vamp-plugins:bbc-spectral-flux
- URL:        https://github.com/bbc/bbc-vamp-plugins
- Block size: 1024
- Step size:  1024
- Parameter (default):
    - Use L2 norm over L1 (False)
- Outputs:
    - spectral-flux
    
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
    - skewness

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
