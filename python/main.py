from raspi_import import raspi_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('/home/gruppe22/Documents/TTT4280-Project/C/build/out-2025-01-30-18.35.24.bin')

SAMPLE_COUNT = 31250

#Make lists for data channels
numSamplesPlot = 1000
c1 = np.zeros(numSamplesPlot)
c2 = np.zeros(numSamplesPlot)
c3 = np.zeros(numSamplesPlot)
c4 = np.zeros(numSamplesPlot)
c5 = np.zeros(numSamplesPlot)

#Put data from channels into corresponding lists
for i in range(numSamplesPlot):
    c1[i] = data[i][0]*0.81*10**-3
    c2[i] = data[i][1]*0.81*10**-3
    c3[i] = data[i][2]*0.81*10**-3
    c4[i] = data[i][3]*0.81*10**-3
    c5[i] = data[i][4]*0.81*10**-3

#Make fft
c1f = np.fft.rfft(c1)
c2f = np.fft.rfft(c2)
c3f = np.fft.rfft(c3)

#Make frequency axis
sampfreq = 1/sample_period
freqAxStep = sampfreq/numSamplesPlot
freq = np.arange(0, sampfreq/2 + freqAxStep, freqAxStep)

#X-axis with samples as unit
x = np.arange(0, numSamplesPlot)

ax = plt.subplot()
#ax.plot(x[1:], c1[1:], color = 'red', label = 'channel1')
#ax.plot(x[1:], c2[1:], color = 'blue', label = 'channel2')
ax.plot(x[1:], c2[1:], color = 'orange', label = 'channel2')
# ax.plot(x, c4, color = 'black', label = 'channel4')
# ax.plot(x, c5, color = 'yellow', label = 'channel5')
ax.legend(loc = 'upper right')
plt.title('Measured values')
ax.set_xlabel('Sample')
ax.set_ylabel('Volt [V]')
plt.savefig('lab1Plot_c2')

# plt.title("FFT of samples")
# plt.plot(freq[1:],  20 * np.log10(2 / SAMPLE_COUNT * np.abs(c3f[1:])), color = 'red', label = 'channel')
# plt.legend(loc = 'upper right')
# plt.ylim(-100, 0)
# plt.savefig('lab1_1000kHz_c3')