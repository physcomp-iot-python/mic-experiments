import numpy as np
from matplotlib import pyplot as plt
from scipy import signal,fft
import serial

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
ax  = fig.add_subplot(111)

#discard stale data in buffers
ser.flush()
#discard the first line which may be broken
get_data(ser)
#initialize plot with first dataset
ts, samples = get_data(ser)
graph = ax.plot(samples)[0]

Ymax = 0
Ymin = 0

try:
    while True:
        try:
            ts, samples = get_data(ser)
            graph.set_xdata(np.arange(len(samples)))
            graph.set_ydata(samples)
            Smin = samples.min()
            Smax = samples.max()
            if Smin < Ymin:
                Ymin = Smin
                ax.set_ylim(Ymin, Ymax)
            if Smax > Ymax:
                Ymax = Smax
                ax.set_ylim(Ymin, Ymax)
            plt.draw()
            plt.pause(0.01)
        except ValueError as e:
            print("Caught exception: %s" % e)
            
except KeyboardInterrupt:
    pass
    

