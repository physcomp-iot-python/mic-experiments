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

# Number of samples to read at once.
NUM_SAMPLES = 160
MEDFILT_WINDOW_SIZE = 5  #note should be odd!

#initialize microphone
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, frequency=16000, bit_depth=16)
#array to hold samples and filtered
buff1 = array.array('H', [0] * NUM_SAMPLES)
buff2 = array.array('H', [0] * NUM_SAMPLES)
while True:
    #print(gc.mem_free())
    print(time.monotonic(),end = " ")
    mic.record(buff1, NUM_SAMPLES)
    #run the median filter
    for i in range(MEDFILT_WINDOW_SIZE,NUM_SAMPLES):
        buff2[i] = sorted(list(buff1[i-MEDFILT_WINDOW_SIZE:i]))[MEDFILT_WINDOW_SIZE//2]
    print(" ".join(str(s) for s in buff2))

