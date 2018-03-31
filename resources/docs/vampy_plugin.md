## VAMP Plugins

### bbc-vamp-plugins:bbc-energy
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  1024
Parameter (default):
    - Moving average window size (1.0 seconds)
    - Moving average percentile (3.0)
    - Dip threshold (3.0)
    - Low Energy threshold (1.0)

### bbc-vamp-plugins:bbc-intensity
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  1024
Parameter (default):
    - Sub-bands (7.0)
    - Window shape (Hann)

### bbc-vamp-plugins:bbc-rhythm
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  256
Parameter (default):
    - Sub-bands (7)
    - Threshold (1)
    - Moving avg window len (200 frames)
    - Onset peak window length (6 frames)
    - Min BPM 12
    - Max BPM 300
    
### bbc-vamp-plugins:bbc-spectral-contrast
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  512
Parameter (default):
    - Alpha (0.02)
    - Sub-bands (7)

### bbc-vamp-plugins:bbc-spectral-flux
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  1024
Parameter (default):
    - Use L2 norm over L1 (False)
    
### bbc-vamp-plugins:bbc-speechmusic-segmenter
URL:        https://github.com/bbc/bbc-vamp-plugins
Block size: 1024
Step size:  1024
Parameter (default):
    - Resolution (256)
    - Change threshold (0.08)
    - Decision threshold (0.27)
    - Minimum music segment length (0.0)
    - Margin (14.0)

### beatroot-vamp:beatroot
URL:        https://code.soundsoftware.ac.uk/projects/beatroot-vamp
Block size: 2048
Step size:  441
Parameter (default):
    - Pre-Margin factor (0.15)
    - Post-Margin factor (0.3)
    - Maximum Change (0.2)
    - Expiry Time (10.0)
