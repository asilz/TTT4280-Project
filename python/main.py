from raspi_import import raspi_import
import math_import
import matplotlib.pyplot as plt
import numpy as np

sample_period, data = raspi_import('/home/gruppe22/Documents/TTT4280-Project/C/measurements/lab4_forward1/out-2025-03-24-12.23.17.bin')

#Number of samples
SAMPLE_COUNT = 31250*2
#Time passed between each sample (time of CLK-cycle * cycles per sample)
dt = 1/(31.25*10**3)

#Number of data points that will be plotted
numSamplesPlot = SAMPLE_COUNT



#Make lists for data channels
# c1 = np.zeros(numSamplesPlot)
# c2 = np.zeros(numSamplesPlot)
# c3 = np.zeros(numSamplesPlot)
c4 = np.zeros(numSamplesPlot)
c5 = np.zeros(numSamplesPlot)

#Put data from channels into corresponding arrays
for i in range(SAMPLE_COUNT):
    # c1[i-10] = data[i][0]*0.81*10**-3 - 3.3/2
    # c2[i-10] = data[i][1]*0.81*10**-3 - 3.3/2
    # c3[i-10] = data[i][2]*0.81*10**-3 - 3.3/2
    c4[i] = data[i][3]*0.81*10**-3 - 3.3/2
    c5[i] = data[i][4]*0.81*10**-3 - 3.3/2

#Make fft
# c1f = np.fft.rfft(c1)
# c2f = np.fft.rfft(c2)
# c3f = np.fft.rfft(c3)
#c4f = np.fft.rfft(c4)
#c5f = np.fft.rfft(c5)

#Make frequency axis for FFT
sampfreq = 1/sample_period
freqAxStep = sampfreq/SAMPLE_COUNT
freq = np.arange(0, sampfreq/2 + freqAxStep, freqAxStep)

#X-axis with samples as unit
x = np.arange(-numSamplesPlot, numSamplesPlot-1, 1)
#t-axis with time since first sample as unit
t = np.arange(0, SAMPLE_COUNT*dt, dt)

sin_sig = np.sin(1000*t)

sin_ref = np.sin(1000*2*np.pi*t) + 1


#Making the fft of radar
I = c5[(numSamplesPlot//2):]
Q = c4[(numSamplesPlot//2):]*1j

y = I+Q

y_fft = np.fft.fft(y)
x_fft = np.fft.fftfreq(n = y_fft.size, d = dt)
y_fft = np.fft.fftshift(y_fft)
x_fft = np.fft.fftshift(x_fft)

#Create figure and add the two plots we want
fig = plt.figure()

#Plots are added in positions 1 and 3 to create sapce for axis labels and such
# c1_ax = fig.add_subplot(3, 2, 2)
# c2_ax = fig.add_subplot(3, 2, 4)
# c3_ax = fig.add_subplot(3, 2, 6)
c4_ax = fig.add_subplot(3,1,1)
c5_ax = fig.add_subplot(3,1,2)
radar_fft = fig.add_subplot(3,1,3)
#fft1_ax = fig.add_subplot(3, 2, 2)
#fft2_ax = fig.add_subplot(3, 2, 4)
#fft3_ax = fig.add_subplot(3, 2, 6)
# cross_ax1 = fig.add_subplot(3, 2, 1)
# cross_ax2 = fig.add_subplot(3, 2, 3)
# cross_ax3 = fig.add_subplot(3, 2, 5)



# Plotting the samples
# c1_ax.plot(t[:numSamplesPlot], c1[:numSamplesPlot], color = 'red', label = 'channel1')
# c2_ax.plot(t[:numSamplesPlot], c2[:numSamplesPlot], color = 'blue', label = 'channel2')
# c3_ax.plot(t[:numSamplesPlot], c3[:numSamplesPlot], color = 'orange', label = 'channel3')
c4_ax.plot(t[1:], c4[1:], color = 'red', label = 'Q')
c5_ax.plot(t[1:], c5[1:], color = 'blue', label = 'I')

radar_fft.plot(x_fft, y_fft, color = 'black', label = 'fft of radar')


# cross1 = math_import.cross_correlate(c2, c1)
# cross2 = math_import.cross_correlate(c3, c1)
# cross3 = math_import.cross_correlate(c3, c2)
# cross_ax1.plot(x[numSamplesPlot-200:numSamplesPlot+200], cross1[numSamplesPlot-200:numSamplesPlot+200], color = 'red', label = 'channel1vs2')
# cross_ax2.plot(x[numSamplesPlot-200:numSamplesPlot+200], cross2[numSamplesPlot-200:numSamplesPlot+200], color = 'blue', label = 'channel1vs3')
# cross_ax3.plot(x[numSamplesPlot-200:numSamplesPlot+200], cross3[numSamplesPlot-200:numSamplesPlot+200], color = 'orange', label = 'channel2vs3')

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
c4_ax.set_xlabel('Time [t]')
c4_ax.set_ylabel('Volt [V]')
# c4_ax.yaxis.tick_right()
c5_ax.set_xlabel('Time [t]')
c5_ax.set_ylabel('Volt [V]')
radar_fft.set_xlabel('Frequency [Hz]')
radar_fft.set_ylabel('Magnitude(?) [?]')
radar_fft.set_xlim(-50, 50)

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

plt.savefig('Lab4_rawData_with_fft')

dopp_shift = np.argmax(abs(y_fft)) - len(y_fft) / 2
speed = dopp_shift*(15/2413)

print(f'Objektets hastighet: {round(speed, 2)} m/s. Positiv retning er MOT radaren')

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


# n21 = math_import.find_delay_in_samples(c2, c1)
# n31 = math_import.find_delay_in_samples(c3, c1)
# n32 = math_import.find_delay_in_samples(c3, c2)
# print(n21)
# print(n31)
# print(n32)
# #print(math_import.find_delay_in_seconds(c2,c1, sampfreq))
# #print(math_import.find_delay_in_seconds(c3,c1,sampfreq))
# #print(math_import.find_delay_in_seconds(c3,c2,sampfreq))
# print(math_import.calculate_angle(n31, n21, n32))

