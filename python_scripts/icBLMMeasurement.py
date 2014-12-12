'''Various Imports'''
import sys, os
pydir = 'C:\\Users\\labor\\Frascati_2014_readout\\'
sys.path.append(os.path.join(pydir,'python_scripts\\sub_scripts'))

import threading #Enables the threading.Timer function to time the execution
import numpy as np
import matplotlib.pyplot as plt
import visa as pv  #Handles the GPIB communication
import time as tm  #Only used for sleep command and getting the timestamp
import pandas as pd  #Data frame for data management.
import keithley_func as kf


#Important global variable to halt processing.
global KillSignal


class icBLM:
    def __init__(self):
        #Generate various arrays for measurement.
        self.outArray = pd.DataFrame({'Q':[],
                                 't':[]},#tm.time()]},
                                 columns = ['Q', 't'])
        
        #This number describes the amounts of triggers, between each save of the datafile.
        self.TriggersPerMeasurement =20
        #This number describes the number of samples taken, per trigger.
        self.SamplesPerTrigger =50 #Shouldn't be changed.
        
        #The product of the two cannot be more than 15000. (The total memorydepth of the keithley,
        #    recording nothing more than the time and charge.)
        self.SamplesPerMeasurement = self.TriggersPerMeasurement*self.SamplesPerTrigger
        
        
        #Setup Keithley for measurement, and check connection.
        rm = pv.ResourceManager()
        self.kt = rm.get_instrument('GPIB::24')
        self.kt.write('*IDN?')
        print '\n\n\n', self.kt.read(), 'is initiated - Prepare for vogon poetry!\n\n\n'
        self.kt.write('*rst')
        self.kt.write('*cls')
        
        #Setup system state
        self.kt.write('system:zcheck 0')
        self.kt.write('system:zcheck 1')
        self.kt.write('system:zcheck 0') #It's most likely unnecessary to do more than
        # turning the zero-check off, but I quite like the clickety-sound it makes.
        self.kt.write('system:lsync:state 0') #Turns off synchronisation with the line voltage.
        #Important, if a high samplerate is desired.
        
        self.kt.write('sense:function \'charge\'')
        self.kt.write('sense:charge:range 2e-6')
        self.kt.write('sense:charge:nplc 0.01') #Sample-time; 0.01 power-line-cycles.
        self.kt.write('sense:charge:digits 7') #Resolution set to maximum
        self.kt.write('calculate:state 0') #Turn off all math, for speed
        self.kt.write(':display:enable 0') #Squeeze that last bit of sample-rate out, 
        #  by disabling the display. It leaves a nice star on the display, though.. 
        
        self.kt.write(':charge:adischarge:state 1') #Activate the auto-discharge..
        self.kt.write(':charge:adischarge:level 1.0e-6') # .. and set the threshold.
        
        ###Trigger setup:
        '''Spicy stuff, that is. The principle is as follows:
        1) Skip the first of three layers of control; layer1. We don't need that anyway.
        
        2) Wait for trigger, from the external trigger input (the triglink). When that
        fires, all hell breaks loose. Or at least, it goes on, and takes 
        n = 'SamplesPerMeasurement' points.
        
        It is furthermore limited to activate the trigger more than 
        n = 'TriggersPerMeasurement' times, to keep that thang under control!
        Kidding aside, it's to end it in a reasonable time.
        
        
        '''
        self.kt.write(':arm:layer1:source immediate')
        
        #Sets the number of triggers per Measurement (nMeasurement)
        self.kt.write(':arm:layer2:count ' + str(self.TriggersPerMeasurement)) 
        
        self.kt.write(':arm:layer2:source tlink')
        self.kt.write(':arm:layer2:tconfigure:asynchronous:iline 5') #Set the input
                                                            # line for the triglink
        
        #Sets the number of samples per trigger
        self.kt.write(':trigger:count ' + str(self.SamplesPerTrigger))
        
        self.kt.write('trace:points ' + str(self.SamplesPerMeasurement))
        
        #Sets up the timestamp. It's an absolute format (a lot of digits), and relative to the start.
        self.kt.write('trace:tstamp:format absolute')
        self.kt.write('system:tstamp:type relative')
        self.kt.write('trace:elements tstamp')
        
        self.kt.write('trace:feed:control next') #Control, for taking succesive samples, and saving, upon trigger.
        tm.sleep(3) #COMPUTER DO SOMETHING!
    

filename = 'D:\\Frascati\\data\\electrometer\\Measurement_icBLM'+str(int(tm.time()))
ic = icBLM()
nMeasurement = 0
while nMeasurement < 121:  #Important setting - the maximum number of triggers per run
    
    #Start the aquisition
    ic.kt.write('trace:feed:control next')
    ic.kt.write('init')
    
    isMeasuring = True
    t0 = tm.time()
    while isMeasuring == True:
        #The beauty. Monitors the status registers, and waits for a 'full memory'-flag.
        n = bin(int(str(ic.kt.ask(':status:measurement:event?'))[:-1]))[2:]
        try:
            if n[-10] == '1':
                #This loop waits for the measurement to be indicated finished. When that
                #happens, a flag is set, and the loop is finished.
                print 'Measurement-step finished - saving in array as ' + filename
                q = kf.list2pandasCharge(ic.kt.ask_for_values('trace:data?'), t0)
                ic.outArray = ic.outArray.append(q, ignore_index = True)
                isMeasuring = False #Ends the loop.
                
        except IndexError: #It'd crash a lot, if this wasn't there. As in A LOT.
            pass
    nMeasurement = nMeasurement + 1
    ic.outArray.to_pickle(filename) #Save the data. Note that this happens fairly often. Clever feature.

#For the sake of curiosity, this enables you to see what you're actually measuring. Nifty. 
plt.plot(ic.outArray['t'], ic.outArray['Q'], 'x')
plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    