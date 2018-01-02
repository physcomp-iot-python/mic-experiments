import numpy as np
from matplotlib import pyplot as plt
from scipy import signal,fft
import serial


N_FFT = 256
SAMPLE_RATE = 16e3
MEDFILT_WINDOW_SIZE = 5

def get_data(serial_obj):
    line = serial_obj.readline().strip()
    #print(line)
    line = line.split(" ")
    ts = float(line[0])
    samples = np.array([float(s) for s in line[1:]])
    #print(samples)
    return (ts, samples)

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)

#set up live plotting
plt.ion()
fig = plt.figure()
ax1  = fig.add_subplot(211)
ax2  = fig.add_subplot(212)

#discard stale data in buffers
ser.flush()
#discard the first line which may be broken
get_data(ser)
#initialize plot with first dataset
ts, samples = get_data(ser)
S = samples
F, P = signal.welch(S,fs=SAMPLE_RATE, nfft=N_FFT)
graph1 = ax1.plot(S)[0]
graph2 = ax2.plot(F,P)[0]

#add peak detection
peak_x = P.argmax()
peak_y = P.max()
peak_f = F[peak_x]
peak_text = ax2.text(1.1*peak_f, peak_y, "%d Hz" % peak_f)

try:
    while True:
        try:
            ts, samples = get_data(ser)
            S = samples[MEDFILT_WINDOW_SIZE:] #discard first zeroed entries
            Smean = S.mean()
            Sstd  = S.std()
            F, P = signal.welch(S,fs=SAMPLE_RATE, nfft=N_FFT)
            Pmax = P.max()
            graph1.set_xdata(np.arange(len(S)))
            graph1.set_ydata(S)
            graph2.set_xdata(F)
            graph2.set_ydata(P)
            ax1.set_ylim(Smean - 3*Sstd, Smean + 3*Sstd)
            ax2.set_ylim(0, 1.1*Pmax)
            #add peak detection
            peak_x = P.argmax()
            peak_y = P.max()
            peak_f = F[peak_x]
            peak_text.set_position((1.1*peak_f, peak_y))
            peak_text.set_text("%d Hz" % peak_f)
            plt.draw()
            plt.pause(0.01)
        except ValueError as e:
            print("Caught exception: %s" % e)
            
except KeyboardInterrupt:
    pass
    

