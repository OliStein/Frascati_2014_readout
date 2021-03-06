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
import calendar
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
        
    
    def selector(self,detector,data_header,det_def_list,pflag):
        g.tprinter('running selector',pflag)
        
        col = 0
        if detector == det_def_list[0,0]:
            try:
                col  = np.where(data_header == det_def_list[0,1])[0][0]
                g.printer(det_def_list[0,0]+' data, '+det_def_list[0,1]+' found',pflag)
            except:
                g.printer('no data in '+det_def_list[0,1]+', no '+det_def_list[0,0],pflag)
                self.sel_flag = 0
                
        elif detector == det_def_list[1,0]:
            try:
                col  = np.where(data_header == det_def_list[1,1])[0][0]
                g.printer(det_def_list[1,0]+' data, '+det_def_list[1,1]+' found',pflag)
            except:
                g.printer('no data in '+det_def_list[1,1]+', no '+det_def_list[1,0],pflag)
                self.sel_flag = 0
        if detector == det_def_list[2,0]:
            try:
                col  = np.where(data_header == det_def_list[2,1])[0][0]
                g.printer(det_def_list[2,0]+' data, '+det_def_list[2,1]+' found',pflag)
            except:
                g.printer('no data in '+det_def_list[2,1]+', no '+det_def_list[2,0],pflag)
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
    def moving_average(self, a, n= 3, end = 2000):
#         g.tprinter('running moving average for ',pflag)
        kernel = np.ones(n)/float(n)
        out = sig.fftconvolve(a,kernel,mode = 'same')
        med = np.median(a[-end:])
        #To ensure less discontinuity at the ends, the median value is repeated:
        out[:n] = med
        out[-n:] = med
        return out

    
    # Binary search algorithm:    
    def binarysearch(A, value, imax):
        imin = 0
        while imax >= imin:
            imid = int((imax+imin)/2)
            if A[imid] > value:
                imax = imid - 1
            elif A[imid] < value:
                imin = imid + 1
            else:
                break
        return imid
    
    # Flattens the data 
    def flatten_data(self,detector,coln,window,pflag):
        g.tprinter('running flatten_data for '+detector+' detector',pflag)
        f_data = self.moving_average(self.data[:,coln],window,2*window)
        self.data[:,coln] = f_data
        

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
        g.tprinter('running min_finder for '+detector+' detector',pflag)
        input = self.data[:,coln] 
        return np.amin(input)
    
    # inverts data
    def inverter(self,detector,coln,fac,pflag):
        g.tprinter('running inverter for '+detector+' detector',pflag)
        # data will be inverted if the absolute min value is fac times larger then the max value 
        if self.max_finder(detector,coln,0) <= fac*abs(self.min_finder(detector,coln,0)):
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
        
        #n=2000
        n = int(round(.2*len(self.data)))
        
        offset = np.median(self.data[-n:,coln])
        signal = self.data[:,coln] - offset
        noise = signal[-n:]
        
        sigRMS = self.rms(signal,0)
        noiseRMS = self.rms(noise,0)
        
        g.printer('SNR: '+str(sigRMS/noiseRMS),pflag)
        
        out = sigRMS/noiseRMS
        return out 
    
    
    # corrects offset 
    # takes the median of the last n data points and subtracts it from all the data        
    def offset_corr(self,detector,coln,pflag):
        g.tprinter('running offset_corr for '+detector+' detector',pflag)
        #n=2000
        #Takes the last 10% of the data points
        n = int(round(.1*len(self.data)))
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
        #n=2000
        #Takes the last 10% of the data points
        n = int(round(.1*len(self.data)))
        offset = np.median(self.data[-n:,coln])
        signal = self.data[:, coln] - offset
        noise = self.rms(signal[-n:], 0)
        g.printer('noise of '+detector+' detector:',pflag)
        g.printer(noise,pflag)
        return noise
    
    # plots data
    def data_plotter(self,detector,coln,data_header,det_def_list,pflag):
        g.tprinter('running data_plotter for '+detector+' detector',pflag)
        plt.ion()
        plt.clf()
        interval = 200
        f, axarr = plt.subplots(3, sharex = True)
        x = self.data[1:-1:interval,0]
        y1 = self.data[1:-1:interval,sel.selector('dBLM',data_header,det_def_list,1)]
        y2 = self.data[1:-1:interval,sel.selector('icBLM',data_header,det_def_list,1)]
        y3 = self.data[1:-1:interval,sel.selector('WC',data_header,det_def_list,1)]
        axarr[0].plot(x,y1,'r-')
        axarr[0].set_title('dBLM')
        axarr[1].plot(x,y2,'b-')
        axarr[1].set_title('icBLM data')
        axarr[2].plot(x,y3,'g-')
        axarr[2].set_title('WC data')
        # plots only every 100th data point for speed optimization
        
#         plt.xlabel('time (s)')
#         plt.ylabel('signal (V)')
#         plt.title('Data of '+str(detector)+' detector')
#         plt.plot(x[1:-1:100],y[1:-1:100], 'r-')
        
#        plt.axis([0, 6, 0, 20])
        plt.draw()
 
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
        
        
        
#         max_sig = self.max_finder(detector,coln,0)
#         
#         max_sig_pos = np.where(self.data[:,coln]==max_sig)[0][0]
        
#         g.printer(max_sig_pos,pflag)
        
        dtVector = np.diff(self.data[2000:5000, 0])
        
        #g.printer('Standard deviation of timesteps: '+str(np.std(dtVector)),pflag)
        #    -   It was seen that the standard deviation was ~e-24. 
        #        That's good enough.
        # time interval between two data points
        dt = np.mean(dtVector)
        # maximum signal
        max_sig = self.max_finder(detector,coln,0)
        # maximum signal position in data 
        max_sig_pos = np.where(self.data[:,coln]==max_sig)[0][0]
        
        # lower interval in data points from the max. sig. pos.
        low_interval = int(round((lower_limit*10**(-9))/dt))
        
        # lower interval position in data list
        low = max_sig_pos - low_interval
        
        # upper interval in data points from the max. sig. pos.
        up_interval = int(round((upper_limit*10**(-9))/dt))
        g.printer('up_interval'+str(up_interval),pflag)
        g.printer('length self.data'+str(len(self.data)),pflag)
        # upper interval position in data list
        up = max_sig_pos + up_interval
        g.printer('upper interval position in data list'+str(up),pflag)
        # checks if the interval limits lay outside the list
        # lower limit < 0
        # upper limit > len(self.data)
        
        if low < 0:
            low = 0
        else:
            g.printer('up within data length',pflag)
        
        if up >= len(self.data):
            up = len(self.data)-2
            g.printer('setting upper integral limit to len(m.data):'+str(len(self.data)),pflag)
        else:
            g.printer('up within data length',pflag)
        
        
        # some output in console    
        g.printer('integration interval: '+str(lower_limit+upper_limit)+' ns',pflag)
        g.printer('integration time before maximum: '+str(lower_limit)+' ns',pflag)
        g.printer('integration time after maximum: '+str(upper_limit)+' ns',pflag)
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
        
        
        
        
        #FWHM finder. Must be applied after the averaging!
    def fwhm(self, detector, coln, pflag):
        g.tprinter('Running fwhm estimator on '+detector+' detector', pflag)
        sigin = self.data[:,coln]
        
        maxi = np.max(sigin)
        index = 0
        for i in sigin:
            if i == maxi:
                maxindex = index
                break
            index = index + 1
        #Search first boundary from within:
        while sigin[index] > maxi / 2:
            index = index - 1
        IntFirst = index
        #Search last boundary from within:
        index = maxindex
        while sigin[index] > maxi / 2:
            index = index + 1
        IntLast = index

        #Search first boundary from outside:
        index = 0
        while sigin[index] < maxi / 2:
            index = index + 1
        ExtFirst = index

        #Search last boundary from outside:
        index = len(sigin)-1000
        while sigin[index] < maxi / 2:
            index = index - 1
        ExtLast = index

        #Conclusion: The mean between the int/ext estimators is used as the fwhm estimator
        fwhm_S = (ExtLast + IntLast)/2 - (ExtFirst + IntFirst)/2
        
        #Triggering warnings on inaccurate estimators.
        ErrorFirst = (ExtFirst - IntFirst) / float(fwhm_S) * 100
        ErrorFirstWarning = '''WARNING. The accuracy of the first flank estimators
        vary with more than 2%. The difference is '''
        g.printer(ErrorFirstWarning+ str(ErrorFirst) + '%', ErrorFirst>=2)
        
        ErrorLast = (ExtLast - IntLast) / float(fwhm_S) * 100
        ErrorLastWarning = '''WARNING. The accuracy of the latter flank estimators
        vary with more than 10%. The difference is '''
        g.printer(ErrorLastWarning+ str(ErrorLast) + '%', ErrorLast>=10)
        
        Ts = np.mean(np.diff(self.data[0:500,0]))
        g.printer('FWHM estimated:'+ str(fwhm_S * Ts) + 's', pflag)
        return fwhm_S * Ts
        
        
    # by giving the attenuation factor in db it calculates the real signal height     
    def amp_calc(self,detector,coln,amp,pflag):
        try:
            g.tprinter('running amp_clac for '+detector+' detector',pflag)
            g.printer('the amplification/attenuation is '+str(int(amp))+' dB',pflag)
        except ValueError:
            pass
        out = 10**(float(amp)/20)
        g.printer('the resulting factor is: '+str(out),pflag)
        return out
    
    # by giving the attenuation factor (attenuator (and shunt)) it will correct signal in self.data to the real height
    def data_amp_corr(self,detector,coln,amp_fac,pflag):
        g.tprinter('running data_amp_corr for '+detector+' detector',pflag)
        g.printer('correcting data with the amp_fac of '+str(int(amp_fac)),pflag)
        for i in self.data:
                i[coln] = i[coln]*(amp_fac)
    
    # by giving if a shunt was used it will return the shunt attenuation factor shunt_att            
    def shunt_calc(self,detector,coln,shunt,pflag):
        try:
            g.tprinter('running shunt_calc for '+detector+' detector',pflag)  
            
            if int(shunt) == 1:            
                shunt_att = 51
                g.printer('shunt att:'+str(shunt_att),pflag)
                g.printer('shunt used',pflag)
            else:
                g.printer('no shunt used',pflag)
                shunt_att = 1
        except ValueError:
            pass
            
        return shunt_att
    
    # by giving the integral the charge can be calculated with the circuit resistance
    # fac is a conversion factor, might be important for the WC
    def charge_calculator(self,detector,coln,integral,fac,pflag):
        g.tprinter('running charge calculator for '+detector+' detector',pflag)
        # resistance of the circuit 
        res = 50
        charge = fac*float(integral) / res  #Presently set for real measurements.
        g.printer('the measured charge is: '+str(charge),pflag)   
        return charge 
    
    # by giving the charge and a conversion factor the number of particles is calculated
    def ppb_calc(self,detector,coln,charge,conversion,pflag):
        g.tprinter('running ppb_calc for '+detector+' detector',pflag)
        g.printer('the measured charge is: '+str(charge),pflag)
        g.printer('the conversion factor for particle per coulomb is:'+str(conversion),pflag)
        
        ppb = round(float(charge)/float(conversion))
        g.printer('the calculated number of particle per shot is :'+str(ppb),pflag)
        return ppb
    
    # sets data column to zeros        
    def set_data_zero(self):
        for i in self.data:
            i[1] = 0
            
            
    def UTCtimestamp(self, dateColumn, timeColumn, pflag):
        g.tprinter('Generating UTC timestamp',pflag)
        g.printer('Read date is: '+str(dateColumn),pflag)
        g.printer('Read time is: '+str(timeColumn),pflag)
        if len(str(dateColumn)) == 7:
            date = '0'+str(dateColumn)
        elif len(str(dateColumn)) == 8:
            date = str(dateColumn)
        else:
            date = str(dateColumn)
            print 'Fatal error occured in length of date stamp:'
            print date+' with length '+str(len(date))
            sys.exit('0')
        dstamp = calendar.timegm(time.strptime(date,'%d%m%Y'))
        #Reading the time stamp
        #  The 1970 is added to have a correct reference to the unix 
        #   epoch timestamp.
        print timeColumn
        tstamp = calendar.timegm(
                time.strptime('1970:'+str(timeColumn),
                         '%Y:%H:%M:%S'))
        g.printer('The calculated UTC timestamp is '+str(dstamp+tstamp),pflag)
        return dstamp+tstamp
    
    
    
    def detector_current(self,detector,coln,charge,time,pflag):
        g.tprinter('Running detector current calculation for '+detector+' detector',pflag)
        curr = float(charge)/float(time)
        g.printer('The detector current over '+str(time)+'seconds is'+str(curr)+' Ampere',pflag)
        return curr
    
    def max_detector_current(self,detector,coln,max_sig,res,pflag):
        g.tprinter('Running  max detector current calculation for '+detector+' detector',pflag)
        
        curr = float(max_sig)/float(res)
        g.printer('The detector current over 1 second is'+str(curr)+' Ampere',pflag)
        return curr
    
    def sat_detection(self,detector,coln,pflag):
        g.tprinter('Running saturation detection for '+detector+' detector',pflag)
        pass
    
            
