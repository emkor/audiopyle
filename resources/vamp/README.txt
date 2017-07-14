
Vamp
====

An API for audio analysis and feature extraction plugins.

   http://www.vamp-plugins.org/

Vamp is an API for C and C++ plugins that process sampled audio data
to produce descriptive output (measurements or semantic observations).


Vamp Example Plugins Package
============================

 - ZeroCrossing calculates the positions and density of zero-crossing
 points in an audio waveform.

 - SpectralCentroid calculates the centre of gravity of the frequency
 domain representation of each block of audio.

 - PowerSpectrum calculates a power spectrum from the input audio.
 Actually, it doesn't do any work except calculating power from a
 cartesian complex FFT output.  The work of calculating this frequency
 domain output is done for it by the host or host SDK; the plugin just
 needs to declare that it wants frequency domain input.  This is the
 simplest of the example plugins.

 - AmplitudeFollower is a simple implementation of SuperCollider's
 amplitude-follower algorithm.

 - PercussionOnsetDetector estimates the locations of percussive
 onsets using a simple method described in "Drum Source Separation
 using Percussive Feature Detection and Spectral Modulation" by Dan
 Barry, Derry Fitzgerald, Eugene Coyle and Bob Lawlor, ISSC 2005.

 - FixedTempoEstimator calculates a single beats-per-minute value
 which is an estimate of the tempo of a piece of music that is assumed
 to be of fixed tempo, using autocorrelation of a frequency domain
 energy rise metric.  It has several outputs that return intermediate
 results used in the calculation, and may be a useful example of a
 plugin having several outputs with varying feature structures.

See http://vamp-plugins.org/plugin-doc/vamp-example-plugins.html for
more documentation about these plugins.


Installation
============

To install these plugins, copy the files vamp-example-plugins.dylib
and vamp-example-plugins.cat to one of the following directories:

   /usr/local/lib/vamp/
   $HOME/vamp/

You should then be able to use the plugins from within a Vamp host,
such as Sonic Visualiser or the command-line host included with the SDK.


Authors
=======

Vamp, the Vamp SDK and the Vamp example plugins were designed and made
at the Centre for Digital Music at Queen Mary, University of London.

The SDK was written by Chris Cannam, copyright (c) 2005-2008
Chris Cannam and QMUL.

Thanks to Mark Sandler, Christian Landone, Mark Levy, Dan Stowell,
Martin Gasser, and Craig Sapp.

  
    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR
    ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    Except as contained in this notice, the names of the Centre for
    Digital Music; Queen Mary, University of London; and Chris Cannam
    shall not be used in advertising or otherwise to promote the sale,
    use or other dealings in this Software without prior written
    authorization.

