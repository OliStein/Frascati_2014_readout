'''
Created on 29 Sep 2014

@author: ostein
'''


import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import shutil as st
import pickle 
from time import strftime, localtime
import time
import glob
import matplotlib.pyplot as plt
import scipy.signal as sig
from pylab import *

from gen_class import gen

g = gen()

class data_selector():
    # class for selecting data by giving detector name
    # IMPORTANT set the right detector/channel
    def flag_set(self,pflag):
        g.tprinter('running sel_flag_set',pflag)
        self.sel_flag = 1
    
    def flag_check(self,pflag):
        g.tprinter('running sel_flag_check',pflag)
        if self.sel_flag == 1: 
            out = True
        else:
            out = False
        
        return out 
        
    
    def selector(self,detector,data_header,pflag):
        g.tprinter('running selector',pflag)
        
        col = 0
        if detector == 'dBLM':
            try:
                col  = np.where(data_header == 'Channel 1')[0][0]
                g.printer('dBLM data, Channel 1 found',pflag)
            except:
                g.printer('no data in Channel 1, no dBLM',pflag)
                self.sel_flag = 0
                
        elif detector == 'icBLM':
            try:
                col  = np.where(data_header == 'Channel 4')[0][0]
                g.printer('icBLM data, Channel 3 found',pflag)
            except:
                g.printer('no data in Channel 3, no icBLM',pflag)
                self.sel_flag = 0
        elif detector == 'WC':
            try:
                col  = np.where(data_header == 'Channel 3')[0][0]
                g.printer('WC data, Channel 4 found',pflag)
            except:
                g.printer('no data in Channel 4, no WC',pflag)
                self.sel_flag = 0
        else:
            pass
        return col
    
    
    
sel = data_selector()

class data_math():

    # Calculates rms value of input vector.
    def rms(self, dataInput, pflag):
        g.tprinter('Calculating RMS value of vector', pflag)
        out = 0
        for i in dataInput:
            out = out + i*i #The sum of the squares

        return np.sqrt(out / len(dataInput)) #Dividing by the number of entries, and taking the square root.
    
    
    # Moving average filter implemented with a fft method. 
    #    ~100 times faster than achievable with median filter.
    def moving_average(self, a, n=3, end = 20000):
        kernel = np.ones(n)/float(n)
        out = sig.fftconvolve(a,kernel,mode = 'same')
        med = np.median(a[-end:])
        #To ensure less discontinuity at the ends, the median value is repeated:
        out[:n] = med
        out[-n:] = med
        return out
    
    # makes data as object of math_class
    def data_in(self,data,pflag):
        g.tprinter('running data_in',pflag)
        self.data = data
    
    # finds maximum of data
    def max_finder(self,detector,coln,pflag):
        g.tprinter('running max_finder for '+detector+' detector',pflag)
        input = self.data[:,coln] 
        return np.amax(input)
    
    # finds  minimum of data
    def min_finder(self,detector,coln,pflag):
        g.tprinter('running max_finder for '+detector+' detector',pflag)
        input = self.data[:,coln] 
        return np.amin(input)
    
    # inverts data
    def inverter(self,detector,coln,fac,pflag):
        g.tprinter('running inverter for '+detector+' detector',pflag)
        # data will be inverted if the absolute min value is fac times larger then the max value 
        if self.max_finder(detector,coln,pflag) <= fac*abs(self.min_finder(detector,coln,pflag)):
            for i in self.data:
                i[coln] = i[coln]*(-1) 
        else:
            pass
        
    # tests if the signal to noise ratio is larger than SNRmin    
    def signal_indicator(self,detector,coln,pflag):
        g.tprinter('running signal_indicator for '+detector+' detector',pflag)
        SNRmin = 2
        SNR = self.signal_to_noise(detector, coln, 0)
        if SNR >= SNRmin:
            g.printer('signal is comfortably larger than noise:',pflag)
            g.printer('SNR: '+str(SNR),pflag)
            out = 1
        else:
            g.printer('signal not strong enough',pflag)
            g.printer('SNR: '+str(SNR),pflag)
            out = 0
        return out
   
    
    # gives the signal to noise ratio and writes it to ana_file    
    def signal_to_noise(self,detector,coln,pflag):
        g.tprinter('running signal_to_noise for '+detector+' detector',pflag)
        
        offset = np.median(self.data[-20000:,coln])
        signal = self.data[:,coln] - offset
        noise = signal[-20000:]
        
        sigRMS = self.rms(signal,0)
        noiseRMS = self.rms(noise,0)
        
        g.printer('SNR: '+str(sigRMS/noiseRMS),pflag)
        
        out = sigRMS/noiseRMS
        return out 
    
    
    # corrects offset 
    # takes the median of the last n data points and subtracts it from all the data        
    def offset_corr(self,detector,coln,pflag):
        g.tprinter('running offset_corr for '+detector+' detector',pflag)
        n=20000
        offset = np.median(self.data[-n:,coln])
        g.printer('offset for '+detector+' detector:',pflag)
        g.printer(offset,pflag)
        for i in self.data:
            i[coln] = i[coln]-offset
        
        return offset
    
    # finds noise
    # looks for the max and min val in the last n data points
    def noise_finder(self,detector,coln,pflag):
        g.tprinter('running RMS noise_finder for '+detector+' detector',pflag)
        n = 20000
        offset = np.median(self.data[-n:,coln])
        signal = self.data[:, coln] - offset
        noise = self.rms(signal[-n:], 0)
        g.printer('noise of '+detector+' detector:',pflag)
        g.printer(noise,pflag)
        return noise
    
    # plots data
    def data_plotter(self,detector,coln,pflag):
        g.tprinter('running data_plotter for '+detector+' detector',pflag)

        x = self.data[:,0]
        y = self.data[:,coln]
       
        # plots only every 100th data point for speed optimization
        
        plt.xlabel('time (s)')
        plt.ylabel('signal (V)')
        plt.title('Data of '+str(detector)+' detector')
        plt.plot(x[1:-1:100],y[1:-1:100], 'r-')
        
#        plt.axis([0, 6, 0, 20])
        plt.show()
 
        # Still needed modules: integrator(DONE), FWHM, multiplication mods. 
        #for amplification and attenuation
        #
        
    # module for finding the nearest value in a list  
#     def find_nearest(self,array,value):
#         idx = (np.abs(array-value)).argmin()
#         return array[idx] 
       
    def integrator(self, detector, coln,lower_limit,upper_limit,pflag):
        g.tprinter('Running integrator on '+detector+' detector', pflag)
        
        
        # The estimator for the timestep is the mean of the change of the time.
        # This should be fairly sound. It's probably not necessary with that 
        # large a samplespace in time, but here goes. Printing the standard
        # deviation, just as a check. - Should be Commented out later.
        
        
        
        max_sig = self.max_finder(detector,coln,pflag)
        
        max_sig_pos = np.where(self.data[:,coln]==max_sig)[0][0]
        
        g.printer(max_sig_pos,pflag)
        
        dtVector = np.diff(self.data[2000:10000, 0])
        
        #g.printer('Standard deviation of timesteps: '+str(np.std(dtVector)),pflag)
        #    -   It was seen that the standard deviation was ~e-24. 
        #        That's good enough.
        # time interval between two data points
        dt = np.mean(dtVector)
        # maximum signal
        max_sig = self.max_finder(detector,coln,pflag)
        # maximum signal position in data 
        max_sig_pos = np.where(self.data[:,coln]==max_sig)[0][0]
        
        # lower interval in data points from the max. sig. pos.
        low_interval = int(round((lower_limit*10**(-9))/dt))
        
        # lower interval position in data list
        low = max_sig_pos - low_interval
        
        # upper interval in data points from the max. sig. pos.
        up_interval = int(round((upper_limit*10**(-9))/dt))
        # upper interval position in data list
        up = max_sig_pos + up_interval
        
        # checks if the interval limits lay outside the list
        # lower limit < 0
        # upper limit > len(self.data)
        
        if low < 0:
            low = 0
        else:
            pass
        
        if up > len(self.data):
            up = len(self.data)
        else:
            pass
        
        
        # some output in console    
        g.printer('integration interval: '+str(lower_limit+upper_limit)+' ns',pflag)
        g.printer('integration time before maximum: '+str(lower_limit),pflag)
        g.printer('integration time after maximum: '+str(upper_limit),pflag)
        g.printer('dt:'+str(dt)+'s',pflag)
        g.printer('scope time at max. sig.: '+str(self.data[max_sig_pos,0]),pflag)
        g.printer('scope time for lower limit: '+str(self.data[low,0]),pflag)
        g.printer('scope time for upper limit: '+str(self.data[up,0]),pflag)
#         g.printer(max_sig_pos,pflag)
#         g.printer(dt,pflag)
        
        # integration with limits
        integral = 0.0
        for i in self.data[low:up,coln]:
            integral = integral + i*dt
        
        # integration WITHOUT limits
        integral_2 = 0.0    
        for i in self.data[:,coln]:
            integral_2 = integral_2 + i*dt    
            
            # Logbook day two. This is a bit of clusterfuck.
            # When I run the integration, it invariably spits out an answer which is
            # roughly the orders of magnitude smaller than it should be, compared to
            # the analog calculations I've made with the notebook, and integrating
            # the signal 'normally'. That is, the exact same algorithm, but then, 
            # not at all. I'm really at a loss here. My sanity is starting to fade
            # and the world seems grey and stale. 
            
            #I guess my sanity has always been questionable, and it is a bit after
            # six, so the daylight is not really an applicable concept anymore. 
            
            # Logbook day three. I'm a total and utter cock. I really should get
            # myself together and stop coding, when it gets too late. All of the
            # sudden I'm forgetting how to fucking index a 2D np array. I guess that
            # is the limit of my mental capacity. It doesn't look great. 
            # Seriously doubting my sanity again. Someone should do something. Soon.
            # It works now, by the way. 
            
        g.printer('Integration results within the limits: '+str(integral)+' Vs', pflag)
        g.printer('Integration results over complete signal: '+str(integral_2)+' Vs', pflag)
        return integral
        
    def amp_calc(self,detector,coln,amp,pflag):
        g.tprinter('running amp_clac for '+detector+' detector',pflag)
        g.printer('the amplification/attenuation is '+str(int(amp))+' dB',pflag)
        out = 10**(float(amp)/20)
        g.printer('the resulting factor is: '+str(out),pflag)
        return out
    
    def data_amp_corr(self,detector,coln,amp_fac,pflag):
        g.tprinter('running data_amp_corr for '+detector+' detector',pflag)
        g.printer('correcting data with the amp_fac of '+str(int(amp_fac)),pflag)
        for i in self.data:
                i[coln] = i[coln]*(amp_fac)
               
        
    # sets data column to zeros        
    def set_data_zero(self):
        for i in self.data:
            i[1] = 0
            
