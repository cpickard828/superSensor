import numpy as np
from numpy import arange
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
from math import ceil
class VoiceActivityDetector():
    """ Use signal energy to detect voice activity in wav file """
    
    def __init__(self, wave_input_filename):
        self._read_wav(wave_input_filename)._convert_to_mono()
        self.sample_window = 0.02 #20 ms
        self.sample_overlap = 0.01 #10ms
        self.speech_window = 0.5 #half a second
        self.speech_energy_threshold = 0.5 #60% of energy in voice band
        self.speech_start_band = 300
        self.speech_end_band = 3000
           
    def _read_wav(self, wave_file):
        self.rate, self.data = wf.read(wave_file)
        self.channels = len(self.data.shape)
        self.filename = wave_file
        return self
    
    def _convert_to_mono(self):
        if self.channels == 2 :
            self.data = np.mean(self.data, axis=1, dtype=self.data.dtype)
            self.channels = 1
        return self
    
    def _calculate_frequencies(self, audio_data):
        data_freq = np.fft.fftfreq(len(audio_data),1.0/self.rate)
        data_freq = data_freq[1:]
        return data_freq    
    
    def _calculate_amplitude(self, audio_data):
        data_ampl = np.abs(np.fft.fft(audio_data))
        data_ampl = data_ampl[1:]
        return data_ampl
        
    def _calculate_energy(self, data):
        data_amplitude = self._calculate_amplitude(data)
        data_energy = data_amplitude ** 2
        return data_energy
        
    def _znormalize_energy(self, data_energy):
        energy_mean = np.mean(data_energy)
        energy_std = np.std(data_energy)
        energy_znorm = (data_energy - energy_mean) / energy_std
        return energy_znorm
    
    def _connect_energy_with_frequencies(self, data_freq, data_energy):
        energy_freq = {}
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq
    
    def _calculate_normalized_energy(self, data):
        data_freq = self._calculate_frequencies(data)
        data_energy = self._calculate_energy(data)
        #data_energy = self._znormalize_energy(data_energy) #znorm brings worse results
        energy_freq = self._connect_energy_with_frequencies(data_freq, data_energy)
        return energy_freq
    
    def _sum_energy_in_band(self,energy_frequencies, start_band, end_band):
        sum_energy = 0
        for f in energy_frequencies.keys():
            if start_band<f<end_band:
                sum_energy += energy_frequencies[f]
        return sum_energy
    
    def _median_filter (self, x, k):
        assert k % 2 == 1, "Median filter length must be odd."
        assert x.ndim == 1, "Input must be one-dimensional."
        k2 = (k - 1) // 2
        y = np.zeros ((len (x), k), dtype=x.dtype)
        y[:,k2] = x
        for i in range (k2):
            j = k2 - i
            y[j:,i] = x[:-j]
            y[:j,i] = x[0]
            y[:-j,-(i+1)] = x[j:]
            y[-j:,-(i+1)] = x[-1]
        return np.median (y, axis=1)
        
    def _smooth_speech_detection(self, detected_windows):
        median_window=int(self.speech_window/self.sample_window)
        if median_window%2==0: median_window=median_window-1
        median_energy = self._median_filter(detected_windows[:,1], median_window)
        return median_energy
        
    def convert_windows_to_readible_labels(self, detected_windows, time):
        """ Takes as input array of window numbers and speech flags from speech
        detection and convert speech flags to time intervals of speech.
        Output is array of dictionaries with speech intervals.
        """
        percentTimeTalking = 0
        totalTime = 0
        speech_time = []
        is_speech = 0
        for window in detected_windows:
            if (window[1]==1.0 and is_speech==0): 
                is_speech = 1
                speech_label = {}
                speech_time_start = window[0] / self.rate
                speech_label['speech_begin'] = speech_time_start
                print window[0], speech_time_start
                #speech_time.append(speech_label)
            if (window[1]==0.0 and is_speech==1):
                is_speech = 0
                speech_time_end = window[0] / self.rate
                #MYSTUFF
                totalTime = totalTime + speech_time_end - speech_time_start
                #ENDMYSTUFF
                speech_label['speech_end'] = speech_time_end  
                speech_time.append(speech_label)
                print window[0], speech_time_end
        print totalTime
        ## BEGINNING OF MY STUFF

        ampData = self._calculate_amplitude(self.data)
        print "Average amp: " + str(float(float(sum(ampData))/len(ampData)))
        print "Max amp : " + str(np.amax(ampData))
        print "25 per : " + str(np.percentile(ampData, 25))
        print "Median amp : " + str(np.median(ampData))
        print "75 per : " + str(np.percentile(ampData, 75))
        lenData = len(self.data)
        seconds = lenData * 0.000125
        seconds = round(seconds, 3)
        percentTimeTalking = float(totalTime) / seconds
        percentTimeTalking = round(percentTimeTalking, 3)
        print "Percent: " + `percentTimeTalking`
        speech_label = {}
        #time2 = round(time, 3)
        speech_label['percent_time_w_speech'] = round(percentTimeTalking, 3)
        speech_label['time_started'] = round(float(time), 3)
        speech_label['length_of_recording']= round(float(seconds), 3)
        speech_label["mean_amp"] = round(float(float(sum(ampData))/len(ampData)), 3)
        speech_label["med_amp"] = round(np.median(ampData), 3)
        speech_label["25_amp"] = round(np.percentile(ampData, 25), 3)
        speech_label["75_amp"] = round(np.percentile(ampData, 75), 3)
        speech_label["max_amp"] = round(np.amax(ampData), 3)
        speech_time.append(speech_label)

     
        # BEGIN FREQ CALCUATION 
        
        #self._convert_to_mono()
        #self.rate = self.rate / (2.**15)
        #s1 = self.data
        #n = len(s1)
        #p = fft(s1)
        #nUniquePts = int(ceil(n+1)/2.0)
        #freqArray = arange(0, nUniquePts, 1.0) * (self.rate / n)
        #print "Min frequency: " + str(min(freqArray))
        #print "Max frequency: " + str(max(freqArray))
         
        #print "Average freq: " + str(float(float(sum(freqArray))/len(freqArray)))
        #freqData = self._calculate_frequencies(self.data)
        #print "Min frequency: " + str(min(freqData))
        #print "Max frequency: " + str(max(freqData))
        # END FREQ CALCULATION

        
        #np.mean(freqData**2)
        #print "Average frequency" + str(np.sqrt(np.mean(freqData**2)))
        #print "Avg frequency" + str(float(sum(freqData))/len(freqData))
        
         ## END OF MY STUFF
        return speech_time
      
    def plot_detected_speech_regions(self):
        """ Performs speech detection and plot original signal and speech regions.
        """
        data = self.data
        ## BEGINNING OF MY STUFF
        #print self._median_filter(data, 5001)
        amps = self._calculate_amplitude(self.data)
        mean = sum(amps)/len(amps)
        print mean
        #print "Mean: " + `mean`

        ## END of MY STUFF
        detected_windows = self.detect_speech()
        data_speech = np.zeros(len(data))
        it = np.nditer(detected_windows[:,0], flags=['f_index'])
        while not it.finished:
            data_speech[int(it[0])] = data[int(it[0])] * detected_windows[it.index,1]
            it.iternext()
        plt.figure()
        ## MY STUFF
        counter = 0
        for thing in data_speech:
            #print thing
            if thing != 0:
                counter = counter + 1
        print float(counter)/len(data_speech)
        ## END OF MY STUFF
        #print data_speech
        plt.plot(data_speech)
        #plt.plot(data)
        plt.show()
        return self
       
    def detect_speech(self):
        """ Detects speech regions based on ratio between speech band energy
        and total energy.
        Output is array of window numbers and speech flags (1 - speech, 0 - nonspeech).
        """
        detected_windows = np.array([])
        sample_window = int(self.rate * self.sample_window)
        sample_overlap = int(self.rate * self.sample_overlap)
        data = self.data
        sample_start = 0
        start_band = self.speech_start_band
        end_band = self.speech_end_band
        while (sample_start < (len(data) - sample_window)):
            sample_end = sample_start + sample_window
            if sample_end>=len(data): sample_end = len(data)-1
            data_window = data[sample_start:sample_end]
            energy_freq = self._calculate_normalized_energy(data_window)
            sum_voice_energy = self._sum_energy_in_band(energy_freq, start_band, end_band)
            sum_full_energy = sum(energy_freq.values())
            speech_ratio = sum_voice_energy/sum_full_energy
            # Hipothesis is that when there is a speech sequence we have ratio of energies more than Threshold
            speech_ratio = speech_ratio>self.speech_energy_threshold
            detected_windows = np.append(detected_windows,[sample_start, speech_ratio])
            sample_start += sample_overlap
        detected_windows = detected_windows.reshape(len(detected_windows)/2,2)
        detected_windows[:,1] = self._smooth_speech_detection(detected_windows)
        return detected_windows
