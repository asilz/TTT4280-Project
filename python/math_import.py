import numpy as np

def calculate_angle(n31, n21, n32):
    return np.arctan(np.sqrt(3)*((n31 + n21)/(n31-n21+2*n32)))


def find_delay_in_seconds(signal0, signal1, frequency):
    return (np.argmax(np.abs(np.correlate(signal0,signal1, 'full'))) - len(signal0)) / frequency

def find_delay_in_samples(signal0, signal1):
    return np.argmax(np.abs(np.correlate(signal0,signal1, 'full'))) - len(signal0)

def cross_correlate(signal0, signal1):
    return np.correlate(signal0,signal1, 'full')