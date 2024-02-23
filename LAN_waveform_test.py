import numpy as np
import vxi11

from scipy import interpolate
from numpy import pi
import matplotlib.pyplot as plt

def resample(target_x,data_x,data_y):
  f = interpolate.interp1d(data_x,data_y,bounds_error=False, fill_value=0.)
  out_x = target_x
  out_y = f(target_x)
  return (out_x,out_y)


# change the IP address to your instrument's IP
inst = vxi11.Instrument('TCPIP0::169.254.161.170::INSTR')
print(inst.ask('*IDN?'))

frequency = 500e3 #500kHz
period = 1/frequency
 
v_high_1 = 0.5
v_low_1 = -1*v_high_1
 
v_high_2 = 0.5
v_low_2 = -1*v_high_2

samples = 2**12 # 4096 samples
time=np.linspace(0,period,samples)
 
 
y2=np.sin(time/period*2*pi)**2
y1=-1+2*(time >= 1e-6)

plt.plot(time, y2, label = "ch2")
plt.plot(time, y1, label = "ch1")
plt.show()

val_str_1 = ",".join(map(str,y1))
val_str_2 = ",".join(map(str,y2))

inst.write("SOURCE1:TRACE:DATA VOLATILE,"+ val_str_1)
inst.write("SOURCE1:VOLTAGE:UNIT VPP")
inst.write("SOURCE1:VOLTAGE:LOW {:f}".format(v_low_1))
inst.write("SOURCE1:VOLTAGE:HIGH {:f}".format(v_high_1))
inst.write("SOURCE1:PERIOD {:f}".format(period))

inst.write("SOURCE2:TRACE:DATA VOLATILE,"+ val_str_2)
inst.write("SOURCE2:VOLTAGE:UNIT VPP")
inst.write("SOURCE2:VOLTAGE:LOW {:f}".format(v_low_2))
inst.write("SOURCE2:VOLTAGE:HIGH {:f}".format(v_high_2))
inst.write("SOURCE2:PERIOD {:f}".format(period))