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
    def selector(self,detector,pflag):
        g.tprinter('running selector',pflag)
        
        out = 0
        if detector == 'dBLM':
            out = 2
        elif detector == 'icBLM':
            out = 3
        elif detector == 'WC':
            out = 1
        else:
            pass
        return out
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
    
    
    def min_finder(self,detector,coln,pflag):
        g.tprinter('running max_finder for '+detector+' detector',pflag)
        input = self.data[:,coln] 
        return np.amin(input)
    # inverts data
    def inverter(self,detector,coln,pflag):
        g.tprinter('running inverter for '+detector+' detector',pflag)
        input = self.data[:,coln]
        for i in self.data:
            i[sel.selector(detector,0)] = i[coln]*(-1) 
            
    def offset_corr(self,detector,coln,pflag):
        g.tprinter('running offset_corr for '+detector+' detector',pflag)

        offset = np.mean(self.data[:1000,coln])
        g.printer('offset for '+detector+' detector:',pflag)
        g.printer(offset,pflag)
        for i in self.data:
            i[coln] = i[coln]-offset 
        
        return offset
    
    def noise_finder(self,detector,coln,pflag):
        g.tprinter('running noise_finder for '+detector+' detector',pflag)
        nmax = np.max(self.data[:1000,coln])
        nmin = np.min(self.data[:1000,coln])
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
        
    # sets data column to zeros        
    def set_data_zero(self):
        for i in self.data:
            i[1] = 0
            