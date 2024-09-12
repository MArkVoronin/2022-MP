import numpy as np
import matplotlib.pyplot as plt
from Simplesig import Simplesig

class AmplitudeModulatedSignal(Simplesig):

    def __init__(self, frequency, frequency_discret, time_in_sec, amplitude):
        Simplesig.__init__(self, frequency, frequency_discret, time_in_sec, amplitude)


    def create_eveloping(self, amplitude, frequency):


        eveloping = np.zeros(len(self.time))
        for i in range(len(self.time)):    
            eveloping[i] = amplitude * np.cos(frequency * self.time[i])
        return eveloping

    def create_modulated_signal(self, amplitude, frequency): 


        eveloping = self.create_eveloping(amplitude, frequency)

        for i in range(len(self.time)):
            self.signal[i] = amplitude * (1 + (self.amplitude / amplitude) * self.signal[i]) * eveloping[i] 

        print('Create modulated signal: Done!') 
