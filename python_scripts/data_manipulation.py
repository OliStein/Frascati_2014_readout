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
                col  = np.where(data_header == 'Channel 3')[0][0]
                g.printer('icBLM data, Channel 3 found',pflag)
            except:
                g.printer('no data in Channel 3, no icBLM',pflag)
                self.sel_flag = 0
        elif detector == 'WC':
            try:
                col  = np.where(data_header == 'Channel 4')[0][0]
                g.printer('WC data, Channel 4 found',pflag)
            except:
                g.printer('no data in Channel 4, no WC',pflag)
                self.sel_flag = 0
        else:
            pass
        return col
    
    
    
sel = data_selector()

class data_math():
    
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
        
    # tests if the signal to noise ratio is larger than fac    
    def signal_indicator(self,detector,coln,pflag):
        g.tprinter('running signal_indicator for'+detector+' detector',pflag)
        fac = 3
        smax = self.max_finder(detector,coln,0)
        snoise = self.noise_finder(detector,coln,0)
        if smax >= fac*snoise:
            g.printer('signal '+str(fac)+' times larger than noise',pflag)
            g.printer('SNR: '+str(smax/snoise),pflag)
            out = 1
        else:
            g.printer('signal not strong enough',pflag)
            g.printer('SNR: '+str(smax/snoise),pflag)
            out = 0
        return out
   
    
    # gives the signal to noise ratio and writes it to ana_file    
    def signal_to_noise(self,detector,coln,pflag):
        g.tprinter('running signal_to_noise for '+detector+' detector',pflag)
        smax = self.max_finder(detector,coln,0)
        snoise = self.noise_finder(detector,coln,0)
        g.printer('SNR: '+str(smax/snoise),pflag)
      
        out = smax/snoise
        return out 
    
    
    # corrects offset 
    # takes the mean of the first n data points and subtracts it from all the data        
    def offset_corr(self,detector,coln,pflag):
        g.tprinter('running offset_corr for '+detector+' detector',pflag)
        n=1000
        offset = np.mean(self.data[:n,coln])
        g.printer('offset for '+detector+' detector:',pflag)
        g.printer(offset,pflag)
        for i in self.data:
            i[coln] = i[coln]-offset 
        
        return offset
    
    # finds nois     
    # looks for the max and min val in the first n data points
    def noise_finder(self,detector,coln,pflag):
        g.tprinter('running noise_finder for '+detector+' detector',pflag)
        n = 1000
        nmax = np.max(self.data[:n,coln])
        nmin = np.min(self.data[:n,coln])
        noise = nmax-nmin
        g.printer('noise of '+detector+' detector:',pflag)
        g.printer(noise,pflag)
        return noise
    
    # plots data
    def data_plotter(self,detector,coln,pflag):
        g.tprinter('running data_plotter for '+detector+' detector',pflag)

        x = self.data[:,0]
        y = self.data[:,coln]
       
        # plots only every 100th data point for speed optimization
        plt.plot(x[1:-1:100],y[1:-1:100], 'r-')
#        plt.axis([0, 6, 0, 20])
        plt.show()
 
        # Still needed modules: integrator, FWHM, multiplication mods. 
        #for amplification and attenuation
        #
        #
        
    def amp_calc(self,coln,detector,amp,pflag):
        g.tprinter('running amp_clac for '+detector+' detector',pflag)
        g.printer('the amplification/attenuation is '+str(int(amp))+' dB',pflag)
        out = 10**(float(amp)/20)
        g.printer('the resulting factor is: '+str(out),pflag)
        return out
    
    def data_amp_corr(self,coln,detector,amp_fac,pflag):
        g.tprinter('running data_amp_corr for '+detector+' detector',pflag)
        g.printer('correcting data with the amp_fac of '+str(int(amp_fac)),pflag)
        for i in self.data:
                i[coln] = i[coln]*(amp_fac)
               
        
    # sets data column to zeros        
    def set_data_zero(self):
        for i in self.data:
            i[1] = 0
            