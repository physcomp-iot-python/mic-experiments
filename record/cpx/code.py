# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert for Adafruit Industries
# Copyright (c) 2017 Kattni Rembor, Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import array
import audiobusio
import board
import time
import gc
import math

# Number of samples to read at once.
NUM_SAMPLES = 160
MEDFILT_WINDOW_SIZE = 5  #note should be odd!


#def design_narrow_bandpass(f_hz,bw_hz,sample_rate = 16e3):
#    f  = f_hz/sample_rate
#    bw = bw_hz/sample_rate
#    R = 1.0 - (3.0 * bw)
#    Rsq = R*R
#    cosf2 = 2.0 * math.cos(2.0*math.pi*f)
#    K = (1.0 - R * cosf2 + Rsq ) / (2.0 - cosf2)
#    a0 = 1.0 - K
#    a1 = 2.0 * (K - R)*cosf2
#    a2 = Rsq - K
#    b1 = 2.0*R*cosf2
#    b2 = -Rsq
#    return (a0,a1,a2,b1,b2)


def filter_IIR_ord1(b, a, src, dest):
    assert(len(dest) >= len(src))
    x = src
    y = dest
    x_1 = 0.0
    x_2 = 0.0
    y_1 = 0.0
    y_2 = 0.0
    b0,b1,b2 = b
    a0,a1,a2 = a
    for i in range(len(x)):
        # IIR difference equation
        y[i] = (b0*x[i] + b1*x_1 + b2*x_2 - a1*y_1 - a2*y_2)/a0
        #shift delayed x, y samples
        x_2 = x_1
        x_1 = x[i]
        y_2 = y_1
        y_1 = y[i]
        
#scipy.signal.bessel(1,[0.5e3/8e3,1.5e3/8e3], btype="bandpass")
# 8e3 is Nyquist rate == sample_rate/2
bp_b = [ 0.16591068,  0.        , -0.16591068]
bp_a = [ 1.        , -1.57138992,  0.66817864]

#initialize microphone
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, frequency=16000, bit_depth=16)
#array to hold samples and filtered
samples = array.array('H', [0] * NUM_SAMPLES)
buff1 = array.array('f', [0] * NUM_SAMPLES)
buff2 = array.array('f', [0] * NUM_SAMPLES)
while True:
    #print(gc.mem_free())
    print(time.monotonic(),end = " ")
    mic.record(samples, NUM_SAMPLES)
    #run the median filter with baseline removal -> buff1
    mean_val = float(sum(samples))/NUM_SAMPLES
    for i in range(MEDFILT_WINDOW_SIZE,NUM_SAMPLES):
        med = sorted(list(samples[i-MEDFILT_WINDOW_SIZE:i]))[MEDFILT_WINDOW_SIZE//2]
        buff1[i] = med - mean_val
    #run the bandpass filter -> buff2
    filter_IIR_ord1(bp_b, bp_a, src=buff1, dest=buff2)
    print(" ".join(["%0.6f" % f for f in buff2]))

