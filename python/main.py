from raspi_import import raspi_import
import math_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('/home/gruppe22/Documents/TTT4280-Project/C/measurements/lab2_second_angle/out-2025-02-17-12.54.18.bin')

#Number of samples
SAMPLE_COUNT = 31250
#Time passed between each sample (time of CLK-cycle * cycles per sample)
dt = 1/(31.25*10**3)

#Number of data points that will be plotted
numSamplesPlot = SAMPLE_COUNT - 10



#Make lists for data channels
c1 = np.zeros(SAMPLE_COUNT)
c2 = np.zeros(SAMPLE_COUNT)
c3 = np.zeros(SAMPLE_COUNT)
c4 = np.zeros(SAMPLE_COUNT)
c5 = np.zeros(SAMPLE_COUNT)

#Put data from channels into corresponding arrays
for i in range(SAMPLE_COUNT):
    c1[i] = data[i][0]*0.81*10**-3 - 3.3/2
    c2[i] = data[i][1]*0.81*10**-3 - 3.3/2
    c3[i] = data[i][2]*0.81*10**-3 - 3.3/2
    c4[i] = data[i][3]*0.81*10**-3 - 3.3/2
    c5[i] = data[i][4]*0.81*10**-3 - 3.3/2

#Make fft
#c1f = np.fft.rfft(c1)
#c2f = np.fft.rfft(c2)
#c3f = np.fft.rfft(c3)
#c4f = np.fft.rfft(c4)
#c5f = np.fft.rfft(c5)

#Make frequency axis for FFT
sampfreq = 1/sample_period
freqAxStep = sampfreq/SAMPLE_COUNT
freq = np.arange(0, sampfreq/2 + freqAxStep, freqAxStep)
        
#X-axis with samples as unit
x = np.arange(-SAMPLE_COUNT, SAMPLE_COUNT-1, 1)
#t-axis with time since first sample as unit
t = np.arange(0, SAMPLE_COUNT*dt, dt)

sin_sig = np.sin(1000*t)

sin_ref = np.sin(1000*2*np.pi*t) + 1


#Create figure and add the two plots we want
fig = plt.figure()

#Plots are added in positions 1 and 3 to create sapce for axis labels and such
c1_ax = fig.add_subplot(3, 2, 2)
c2_ax = fig.add_subplot(3, 2, 4)
c3_ax = fig.add_subplot(3, 2, 6)
# c4_ax = fig.add_subplot(1,1,1)
# c5_ax = fig.add_subplot(1,1,1)
#fft1_ax = fig.add_subplot(3, 2, 2)
#fft2_ax = fig.add_subplot(3, 2, 4)
#fft3_ax = fig.add_subplot(3, 2, 6)
cross_ax1 = fig.add_subplot(3, 2, 1)
cross_ax2 = fig.add_subplot(3, 2, 3)
cross_ax3 = fig.add_subplot(3, 2, 5)



# Plotting the samples
c1_ax.plot(t[:numSamplesPlot], c1[:numSamplesPlot], color = 'red', label = 'channel1')
c2_ax.plot(t[:numSamplesPlot], c2[:numSamplesPlot], color = 'blue', label = 'channel2')
c3_ax.plot(t[:numSamplesPlot], c3[:numSamplesPlot], color = 'orange', label = 'channel3')


cross1 = math_import.cross_correlate(c1, c2)
cross2 = math_import.cross_correlate(c1, c3)
cross3 = math_import.cross_correlate(c2, c3)
cross_ax1.plot(x[31000:31500], cross1[31000:31500], color = 'red', label = 'channel1vs2')
cross_ax2.plot(x[31000:31500], cross2[31000:31500], color = 'blue', label = 'channel1vs3')
cross_ax3.plot(x[31000:31500], cross3[31000:31500], color = 'orange', label = 'channel2vs3')

# c4_ax.plot(t[1:numSamplesPlot], c4[1:numSamplesPlot], color = 'black', label = 'channel4')
# c5_ax.plot(t[1:numSamplesPlot], c5[1:numSamplesPlot], color = 'green', label = 'channel5')
# samples_ax.plot(t[1:numSamplesPlot], sin_ref[1:numSamplesPlot], color = 'purple', label = 'sine ref')
#c1_ax.set_xlabel('Time [t]')
#c1_ax.set_ylabel('Volt [V]')
#c2_ax.set_xlabel('Time [t]')
#c2_ax.set_ylabel('Volt [V]')
# c2_ax.yaxis.tick_right()
#c3_ax.set_xlabel('Time [t]')
#c3_ax.set_ylabel('Volt [V]')
# c4_ax.set_xlabel('Time [t]')
# c4_ax.set_ylabel('Volt [V]')
# c4_ax.yaxis.tick_right()
# c5_ax.set_xlabel('Time [t]')
# c5_ax.set_ylabel('Volt [V]')

#c1_ax.legend(loc = 'upper right')
# c1_ax.set_ylim(-0.2, 3.5)
#c2_ax.legend(loc = 'upper right')
# c2_ax.set_ylim(-0.2, 3.5)
#c3_ax.legend(loc = 'upper right')
# c3_ax.set_ylim(-0.2, 3.5)
# c4_ax.legend(loc = 'upper right')
# c4_ax.set_ylim(-0.2, 3.5)
# c5_ax.legend(loc = 'upper right')
# c5_ax.set_ylim(-0.2, 3.5)

plt.savefig('Lab2_cross0_test')

# Plotting the fft of the samples
# fft1_ax.axvline(440)
# fft1_ax.plot(freq[1:],  20 * np.log10(2 / SAMPLE_COUNT * np.abs(c1f[1:])), color = 'red', label = 'channel1_fft')
# fft1_ax.set_xlabel('Frequency [Hz]')
# fft1_ax.set_ylabel('Rel. effect [dB]')
# fft1_ax.set_xlim(0, 600)
#fft1_ax.set_ylim(-100, 20)
#fft1_ax.legend(loc = 'upper right')
#fft1_ax.yaxis.tick_right()

# fft2_ax.axvline(440)
#fft2_ax.plot(freq[1:],  20 * np.log10(2 / SAMPLE_COUNT * np.abs(c2f[1:])), color = 'blue', label = 'channel2_fft')
#fft2_ax.set_xlabel('Frequency [Hz]')
#fft2_ax.set_ylabel('Rel. effect [dB]')
#fft2_ax.set_xlim(0, 600)
#fft2_ax.set_ylim(-100, 20)
#fft2_ax.legend(loc = 'upper right')
#fft2_ax.yaxis.tick_right()

# fft3_ax.axvline(440)
#fft3_ax.plot(freq[1:],  20 * np.log10(2 / SAMPLE_COUNT * np.abs(c3f[1:])), color = 'orange', label = 'channel3_fft')
#fft3_ax.set_xlabel('Frequency [Hz]')
#fft3_ax.set_ylabel('Rel. effect [dB]')
#fft3_ax.set_xlim(0, 600)
#fft3_ax.set_ylim(-100, 20)
#fft3_ax.legend(loc = 'upper right')
#fft3_ax.yaxis.tick_right()

print(math_import.find_delay_in_samples(sin_sig, sin_sig))