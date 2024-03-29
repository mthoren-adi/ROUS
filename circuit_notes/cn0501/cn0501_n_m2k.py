# Copyright (C) 2020 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
print("Program start")

from scipy.signal import periodogram
import matplotlib.pyplot as plt
from adi import ad7768
import numpy as np
import libm2k
import pandas as pd
import math

print("Import done")

N_SAMPLES = 1024

adc = ad7768(uri="ip:10.116.177.40")
adc.sample_rate = 256000
adc.power_mode = "FAST_MODE"
adc.filter = "SINC5"

'''
m2k = libm2k.m2kOpen("ip:192.168.2.1")
m2k.calibrateDAC()
aout = m2k.getAnalogOut()
aout.setSampleRate(0, 750000)
aout.setSampleRate(1, 750000)
aout.enableChannel(0, True)
aout.enableChannel(1, True)
aout.setCyclic(True)

x = np.linspace(-np.pi, np.pi, N_SAMPLES)

w1_p = np.sin(x) + 2.5 
w1_n = np.sin(x + np.pi) + 2.5


buff = [np.array([aout.convertVoltsToRaw(0, item) for item in w1_p], dtype='int16'),
        np.array([aout.convertVoltsToRaw(1, item) for item in w1_n], dtype='int16')]
aout.pushRawBytes(0, buff[0], N_SAMPLES)
aout.pushRawBytes(1, buff[1], N_SAMPLES)
'''
#File directory of exported csv files
fdir = 'C:\Users\VCalinao\pyadi-iio\examples\csv_files\\'

print("Buffer size")
print(adc.rx_buffer_size)

sec_rec = math.ceil(adc.sample_rate/adc.rx_buffer_size)

print("\n How many loops? \n")
loops = int(input())
print("\n What channel? \n")
ch = int(input())
print("\n Export filename? \n")
fname = input()
print("\n TEST START \n")


for nloop in range(0,loops):
    print(nloop)
    vdata = []
    count = 0
    for _ in range(sec_rec):
            #plt.clf()1
            
            #plt.ylim((-5,5))
            data = adc.rx() 
            vdata.append(data[ch])
            count += len(data[ch])
            #for ch in adc.rx_enabled_channels:
            #plt.plot(range(0, adc.rx_buffer_size), data[ch])
            #label = "voltage" + str(ch))
            #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
            #    ncol=2, mode="expand", borderaxespad=0.)
            #plt.pause(0.001)

    vdata_arr = np.asarray(vdata)
    vdata_arr = vdata_arr.reshape(count,1)

    DF = pd.DataFrame(vdata_arr)
    fname = fname + "_loop" + str(nloop)+".csv"
    print(fname)
    DF.to_csv(fdir+fname)
print("Export done")