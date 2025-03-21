import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


muabo = np.genfromtxt("./muabo.txt", delimiter=",")
muabd = np.genfromtxt("./muabd.txt", delimiter=",")



def mua_blood_oxy(x): return np.interp(x, muabo[:, 0], muabo[:, 1])
def mua_blood_deoxy(x): return np.interp(x, muabd[:, 0], muabd[:, 1])





def get_mua(blood_volume_fraction, blood_oxygenation, wavelength):
    mua_other = 25 # Background absorption due to collagen, et cetera
    mua_blood = (mua_blood_oxy(wavelength)*blood_oxygenation # Absorption due to
            + mua_blood_deoxy(wavelength)*(1-blood_oxygenation)) # pure blood
    return mua_blood * blood_volume_fraction + mua_other

# reduced scattering coefficient ($\mu_s^\prime$ in lab text)
# the numerical constants are thanks to N. Bashkatov, E. A. Genina and
# V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
# tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
# Units: 1/m
def get_musr(wavelength):
    return 100 * (17.6*(wavelength/500)**-4 + 18.78*(wavelength/500)**-0.22)

def get_penetration_depth(mua, musr):
    return np.sqrt(1/(3*(musr+mua)*mua))

def diffusion_equation(z, mua, musr):
    return 1/(2*get_penetration_depth(mua,musr)*mua) * np.exp(-np.sqrt(3*mua*(musr+mua))*z)

def get_reflectance(mua, musr):
    return np.sqrt(3*(musr/mua + 1))

def get_contrast(transmittance_high_blood_volume, transmittance_low_blood_volume):
    return np.abs(transmittance_high_blood_volume-transmittance_low_blood_volume)/transmittance_low_blood_volume

def SNR(signal, sampling_frequency):
    fft_y = np.fft.fft(signal)
    fft_x = np.fft.fftfreq(n = fft_y.size, d=1/sampling_frequency)
    target_frequency = fft_x[np.argmax(np.abs(fft_y))]
    result = 0
    for i in range(len(fft_x)):
        if(fft_x[i] < target_frequency + 2/60 and fft_x[i] > target_frequency - 2/60):
            result += np.abs(fft_y[i])
    return result / (np.sum(np.abs(fft_y)))

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def variance(input_array):
    variance = 0
    array_average = np.average(input_array)
    for element in input_array:
        variance += (element - array_average) * (element - array_average)
    return variance/len(input_array)


    
#bvf = 1 # Blood volume fraction, average blood amount in tissue
oxy = 0.8 # Blood oxygenation

red_wavelength = 600 # Replace with wavelength in nanometres
green_wavelength = 520 # Replace with wavelength in nanometres
blue_wavelength = 470 # Replace with wavelength in nanometres
wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

mua001 = get_mua(0.01, oxy, wavelength)
mua1 = get_mua(1.0, oxy, wavelength)
musr = get_musr(wavelength)

transmittance_high_blood_volume = diffusion_equation(300*10**(-6), mua1,musr)/diffusion_equation(0.0, mua1, musr)
transmittance_low_blood_volume = diffusion_equation(300*10**(-6), mua001,musr)/diffusion_equation(0.0, mua001, musr)
print(transmittance_high_blood_volume) # c
print(transmittance_low_blood_volume) # c
print(get_contrast(transmittance_high_blood_volume, transmittance_low_blood_volume)) # c
#print(get_penetration_depth(mua001, musr)) # a
#print(diffusion_equation(0.013, mua001, musr)/diffusion_equation(0.0, mua001,musr)) # b

fig = plt.figure()
red_fft_ax = fig.add_subplot(3, 2, 1)
red_ax = fig.add_subplot(3, 2, 2)
green_fft_ax = fig.add_subplot(3, 2, 3)
green_ax = fig.add_subplot(3, 2, 4)
blue_fft_ax = fig.add_subplot(3, 2, 5)
blue_ax = fig.add_subplot(3, 2, 6)

#np.fft.fft()
SAMPLE_FREQ = 30
SAMPLE_PERIOD = 1/SAMPLE_FREQ
SAMPLE_COUNT = 893 - 6
freqAxStep = SAMPLE_FREQ/SAMPLE_COUNT
freq = np.arange(0, SAMPLE_FREQ/2 + freqAxStep, freqAxStep)

red = np.zeros(SAMPLE_COUNT)
green = np.zeros(SAMPLE_COUNT)
blue = np.zeros(SAMPLE_COUNT)

x = np.arange(0, SAMPLE_COUNT)



with open('data_data', 'r') as file:
    i = 0
    for line in file:
        # Split the line into components
        parts = line.strip().split()
        if len(parts) == 3:
            # Convert each part to float and append to respective array
            red[i] = (float(parts[0]))
            green[i] = (float(parts[1]))
            blue[i] = (float(parts[2]))
            i += 1
            if(i == SAMPLE_COUNT):
                break


red -= np.average(red)
green -= np.average(green)
blue -= np.average(blue)

red = butter_bandpass_filter(red, 0.5, 3, SAMPLE_FREQ)
green = butter_bandpass_filter(green, 0.5, 3, SAMPLE_FREQ)
blue = butter_bandpass_filter(blue, 0.5, 3, SAMPLE_FREQ)

red_fft_y = np.fft.rfft(red)
red_fft_x = freq * 60
red_fft_ax.plot(red_fft_x[1:], np.abs(red_fft_y), color = 'red')

green_fft_y = np.fft.rfft(green)
green_fft_x = freq * 60
green_fft_ax.plot(green_fft_x[1:], np.abs(green_fft_y), color = 'green')

blue_fft_y = np.fft.rfft(blue)
blue_fft_x = freq * 60
blue_fft_ax.plot(blue_fft_x[1:], np.abs(blue_fft_y), color = 'blue')

red_ax.plot(x, red, color = 'red')
green_ax.plot(x, green, color = 'green')
blue_ax.plot(x, blue, color = 'blue')

#print(freq[np.argmax(np.abs(green))])

plt.show()

print(SNR(green, SAMPLE_FREQ))

bpms = np.zeros(4)

for index in range(4):
    string = 'mars3_jugular2_r' + str(index) + '_data'
    with open(string, 'r') as file:
        i = 0
        for line in file:
            # Split the line into components
            parts = line.strip().split()
            if len(parts) == 3:
                # Convert each part to float and append to respective array
                red[i] = (float(parts[0]))
                green[i] = (float(parts[1]))
                blue[i] = (float(parts[2]))
                i += 1
                if(i == SAMPLE_COUNT):
                    break
    red -= np.average(red)
    green -= np.average(green)
    blue -= np.average(blue)

    red = butter_bandpass_filter(red, 0.5, 3, SAMPLE_FREQ)
    green = butter_bandpass_filter(green, 0.5, 3, SAMPLE_FREQ)
    blue = butter_bandpass_filter(blue, 0.5, 3, SAMPLE_FREQ)

    red_fft_y = np.fft.fft(red)
    green_fft_y = np.fft.fft(green)
    blue_fft_y = np.fft.fft(blue)
    
    fft_x = np.fft.fftfreq(n = green_fft_y.size, d=1/SAMPLE_FREQ)
    bpms[index] = fft_x[np.argmax(np.abs(green_fft_y))] * 60
    

print(np.average(bpms))
print(np.sqrt(variance(bpms)))



#print(np.abs(green_fft_y))
