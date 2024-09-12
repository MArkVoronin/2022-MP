from SimpSigGen import SimpSigGen
from AmpModSig import AmpModSig
from Chein import Chein
from Analyzer import Analyzer


modulated_signal = AmpModSig(10, 10000, 40, 5)

modulated_signal.create_garmonic_signal()

signal = modulated_signal.return_the_signal()

modulated_signal.next_selection(99)

modulated_signal.create_modulated_signal(4, 1)

modulated_signal.return_the_signal()

analz = Analyzer(signal, modulated_signal.time)
analz.create_spectrum()


chains = Chein(signal, modulated_signal.time)

signal_f = chains.butter_filter()

anal_f = Analyzer(signal_f, modulated_signal.time)
anal_f.create_spectrum() 