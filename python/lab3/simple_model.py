import numpy as np


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

def get_contrast(reflectance_high_blood_volume, reflectance_low_blood_volume):
    return np.abs(reflectance_high_blood_volume-reflectance_low_blood_volume)/reflectance_low_blood_volume

def SNR(signal, target_frequency, sampling_frequency):
    fft_y = np.fft.fft(signal)
    fft_x = np.fft.fftfreq(n = fft_y.size, d=1/sampling_frequency)
    for i in range(len(fft_x)):
        if(fft_x[i] == target_frequency):
            return np.abs(fft_y[i])/(np.sum(np.abs(fft_y))-np.abs(fft_y[i]))
    return -1

    
#bvf = 1 # Blood volume fraction, average blood amount in tissue
oxy = 0.8 # Blood oxygenation

red_wavelength = 600 # Replace with wavelength in nanometres
green_wavelength = 520 # Replace with wavelength in nanometres
blue_wavelength = 470 # Replace with wavelength in nanometres
wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

mua001 = get_mua(0.01, oxy, wavelength)
mua1 = get_mua(1.0, oxy, wavelength)
musr = get_musr(wavelength)

print(get_contrast(diffusion_equation(300*10**(-6), mua1,musr)/diffusion_equation(0.0, mua1, musr), diffusion_equation(300*10**(-6), mua001,musr)/diffusion_equation(0.0, mua001, musr)))
print(get_penetration_depth(mua001, musr))
print(diffusion_equation(0.013, mua001, musr)/diffusion_equation(0.0, mua001,musr))

x = np.linspace(0,10000)
sig = np.sin(1*x)
print(SNR(sig, 2000, 10000))
