#! c:\Python27\python
'''
Created on 19 Aug 2014

@author: ostein
'''
import sys
import os
import numpy as np

from analysis_modules import log_files
from analysis_modules import data
from analysis_modules import Tee
import matplotlib.pyplot as plt

from csv_list_class import csv_list
from gen_class import gen
from data_manipulation import data_selector
from data_manipulation import data_math
import time as tm


l = log_files()
d = data()
c = csv_list()
# li = lists()
g = gen()
# <<<<<<< HEAD




sel = data_selector()
m  = data_math() 







#++++++++++++++++++++++++++++++++++++++++++++++++++
#--------------------------------------------------
# Important variables 
#--------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------------------------------------------
# PATH OF THE ROOT DIRECTORY
#--------------------------------------------------

# Oliver's mac path
#cwd = '/Users/Oli/work/Frascati/Frascati_2014_readout'

# CHristian's PC path
# cwd = '/home/csoerens/Desktop/python/Frascati_Data_Analysis'

# cwd = 'C:\\Github'

# FLorian's mac path

# Daniel's mac path

# Labor Laptop path
cwd = 'C:\\frascati_data'
#--------------------------------------------------
# DEFINING THE DECTOR'S CHANNELS
#--------------------------------------------------

det_def_list = np.array([['icBLM','Channel 3'],['dBLM','Channel 1'],['WC','Channel 2']])

#--------------------------------------------------
# IMPORTANT FLAGS FOR THE ANALYSIS
#--------------------------------------------------


# set to one if all files to be analyzed
analyze_all = 0

# sets the limit of files to be analyzed
# set to negative value if all sets shall be analyzed
test_limit = -1


# skip files, for improving speed
skip_files = 1

# save interval 
save_int = 10

# set pflag
# pflag = 1 will force modules to print in the log file (recommended) 
# pflag = 0 no output
pflag = 1

# set plotter_flag
# plotter_flag = 1 will force the script to plot every analyzed data
# can slow down the script 
plotter_flag = 0


#--------------------------------------------------
# DONT TOUCH CODE AFTER THIS COMMENT 
#--------------------------------------------------

tstart=tm.time()
data_path = os.path.join(cwd,'data')
sel = data_selector()
m  = data_math() 

# data_path = os.path.join(cwd,'frascati_test_data')

d.folder_check_create(data_path,0)
 
 
l.log_file_set(data_path,'log')
  
f = open(l.log_path(),'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)
  
  
d.check_infra_structure(data_path,pflag)
d.test_data_creator(data_path,pflag)
d.find_data(data_path,pflag)
# d.ana_file_creator(data_path,1)



d.ana_file_deleter(data_path,pflag)

d.ana_file_loader(data_path,pflag)
d.ana_file_loader(data_path,pflag)
d.ana_file_sync(pflag) 
# print len(d.ana_file[0])
d.ana_file_checker(pflag)
# print len(d.ana_file[0])
d.ana_file_saver(data_path,d.ana_file,1,'space',1,pflag)

# Stop here
# sys.exit('stop')

# creates the header with the colum names
header = d.ana_file[0]



# # set to one if all files to be analyzed
# analyze_all = 0


# checks the number of files to be analyzed
naf = c.tba(d.ana_file,analyze_all,pflag)

# # sets the limit of files to be analyzed
# # set to negative value if all sets shall be analyzed
# 
# test_limit = 1


# #skip files, for improving speed
# skip_files = 1


# iterator for 
k = 1

# # save interval 
# save_int = 10

# Stop here
# sys.exit('stop')

#main analysis loop
for i in d.ana_file[1:]:
    # conditions for analyzing the files
    # k is iterator and is limited by test_limit
    # if the file is already analyzed and the flag analyze all is not set, 
    # then only unanalyzed files will be treated
    # when k % skip_files == 0 (modulo), file will be analyzed 
    if (k <= test_limit or test_limit < 0) and ((float(i[c.find_val('analyzed',header,0)])!=1 and k % skip_files == 0)
                                                or analyze_all == 1 ):
        # gives info of the actual file to be analyzed
        g.loop_info(k,naf,1)
        # gives name of file to be analyzed
        g.printer('File to be analyzed:',pflag) 
        g.printer(os.path.split(i[c.find_val('file',header,0)])[-1],pflag)
        
        # loads the data file
        data_comp = c.data_grabber(i,header,3,pflag)
        
        # splits the data in head list and data list
        data_head = np.array(data_comp[:22])
        
        data_header = np.array(data_head[-1])

        # converts data list into a numpy array 
        # last row will be ignored  
        data = np.array(data_comp[23:-1]).astype(float)
        
        # Stop here
#         sys.exit('stop')
        
        # gives the data to data_manipulation class
        m.data_in(data,0)
        
        # writes the time from the scope file into the analysis file
        i[c.find_val('time',header,0)] = data_head[18,2]
        
        
        
        # detector loop
        # runs through the coloumns in the data list and analyses the data
#         det_list = ['icBLM','dBLM','WC']
#         det_def_list = np.array([['icBLM','Channel 3'],['dBLM','Channel 4'],['WC','Channel 2']])
        det_list = det_def_list[:,0]
#         g.printer(det_list,pflag)
        # Stop here
#         sys.exit('stop')
        for det in det_list:
            sel.flag_set(0)
#             i[c.find_val('time',header,0)] = data_head[18,2]
            coln = sel.selector(det,data_header,det_def_list,pflag)
            if sel.flag_check(0):
                
                # is set to 1 if there is data in the scope file
                i[c.find_val(det,header,0)] = 1
                
                # smoothing the data
                # moving_average correction
                # indicates in the analysis file if data is smoothed
                m.flatten_data(det,coln,500,pflag)
                
                i[c.find_val(det+' smoothed',header,0)] = 1
                
                
                # inverts the data if the min value is 2 times smaller than the maximum value
                # the factor can be changed
                m.inverter(det,coln,2,pflag)
                
                # offset correction and writes the offset in the ana_file
                i[c.find_val(det+' offset',header,0)] = m.offset_corr(det,coln,pflag)
                
                # set to one if the signal is fac larger than the noise lvl
                # the fac can be cahbnged in data_anipulation.py in m.signal_indicator
                i[c.find_val(det+' sig.',header,0)] = m.signal_indicator(det,coln,pflag)
                
                # gives the signal to noise ratio and writes it to the ana_file 
                i[c.find_val(det+' SNR',header,0)] = m.signal_to_noise(det,coln,pflag)
                
                #MA-filter of data.
                
                # gives the max data value and writes it to the ana_file
                i[c.find_val(det+' max. sig.',header,0)] = m.max_finder(det,coln,pflag)
            
                i[c.find_val(det+' noise',header,0)] = m.noise_finder(det,coln,pflag)
                

#                 m.data_plotter(det,coln,1)

                # Added to find the fwhm value.
                i[c.find_val(det+' FWHM',header,0)] = m.fwhm(det,coln,pflag)
                
                # detector specific routines
                # not all detectors have a amplification or attenuation
                
                # icBLM
                if  det == 'icBLM':
                    # looks up the attenuation/amplification for the specific detector
                    amp = m.amp_calc(det,coln,i[c.find_val('att. ref.',header,0)],pflag)
                    shunt_att = 1
#                     g.printer(amp,1)
                    
                    i[c.find_val(det+' max sig. att. corr.',header,0)] = shunt_att*amp*float(i[c.find_val('icBLM max. sig.',header,0)])
                    # multiplies the data with the correction factor
                    
#                     m.data_plotter(det,coln,1)
                    # icBLM integration limits
                    lo_limit = 350000
                    up_limit = 350000
                    i[c.find_val(det+' int.',header,0)] = m.integrator(det,coln,lo_limit,up_limit,pflag)
                    i[c.find_val(det+' int. att. corr.',header,0)] = shunt_att*amp*float(i[c.find_val(det+' int.',header,0)])
                    g.printer(i[c.find_val(det+' max sig. att. corr.',header,0)],pflag)
                    i[c.find_val(det+' charge sig.',header,0)] = m.charge_calculator(det, coln, i[c.find_val(det+' int.',header,0)],1,pflag)
                    
                    # Set the conversion factor of the icBLM to 2*10^-16
                    conversion  = float(2*10**(-16))
                    i[c.find_val(det+' ppb',header,0)] = m.ppb_calc(det,coln,i[c.find_val(det+' charge sig.',header,0)],conversion,pflag)
                    # multiplies the data with the correction factor
                    m.data_amp_corr(det,coln,amp*shunt_att,pflag)
                elif det == 'dBLM':
                    amp = m.amp_calc(det,coln,i[c.find_val('att. diamond',header,0)],pflag)
                    shunt_att = m.shunt_calc(det, coln, i[c.find_val('shunt',header,0)], pflag)
                    
                    i[c.find_val(det+' max sig. att. corr.',header,0)] = shunt_att*amp*float(i[c.find_val(det+' max. sig.',header,0)])
                    
                    # multiplies the data with the correction factor
                    
                    
                    # dBLM integration limits
                    lo_limit = 350000
                    up_limit = 350000
                    i[c.find_val(det+' int.',header,0)] = m.integrator(det,coln,lo_limit,up_limit,pflag)
                    i[c.find_val(det+' int. att. corr.',header,0)] = shunt_att*amp*float(i[c.find_val(det+' int.',header,0)])
                    
                    i[c.find_val(det+' charge sig.',header,0)] = m.charge_calculator(det, coln, i[c.find_val(det+' int.',header,0)],1,pflag)
                    # multiplies the data with the correction factor
                    m.data_amp_corr(det,coln,amp*shunt_att,pflag)
                elif det == 'WC':
                    amp = 1
                    shunt_att = 1
                    
                    lo_limit = 10
                    up_limit = 90
                    i[c.find_val(det+' int.',header,0)] = m.integrator(det,coln,lo_limit,up_limit,pflag)
                    i[c.find_val(det+' charge sig.',header,0)] = m.charge_calculator(det, coln, i[c.find_val(det+' int.',header,0)],1,pflag)
                    
                    
                    # added a gain factor of 10 to the conversion for WC
                    conversion = 10*float(1.602*10**(-19))
                    i[c.find_val(det+' ppb',header,0)] = m.ppb_calc(det,coln,i[c.find_val(det+' charge sig.',header,0)],conversion,pflag)
#                     m.data_plotter(det,coln,1)
                    # multiplies the data with the correction factor
                    m.data_amp_corr(det,coln,amp*shunt_att,pflag)   
                    
                else:
                    pass
                # plots the data 
#                 m.data_plotter(det,coln,1)
                
            else:
                pass
        

        if plotter_flag == 1:
            m.data_plotter(det,coln,data_header,det_def_list,pflag)
        else:
            pass
        
#         plt.show()

        # writes the UTC timestamp
        print i[c.find_val('date',header,0)]
        #print d.ana_file
        dateColumn = i[c.find_val('date',header,0)]
        timeColumn = i[c.find_val('time',header,0)]
        i[c.find_val('UTCtime',header,0)] = m.UTCtimestamp(dateColumn, timeColumn, pflag)


        # sets the marker in the ana_file list to analyzed
        i[c.find_val('analyzed',header,0)] = 1
        
        
        
        
        # data list which is saved in ana_data
        data_out = np.concatenate((np.array([data_head[-1]]),m.data),axis = 0)
        
        # saves the analyzed data to ana_data
        c.analyzed_save(header,data_out,i,pflag)
        
        


#         k += 1
#         print data_head

        # saves the ana_file for backup 
        if k % save_int == 0:
            d.ana_file_saver(data_path,d.ana_file,1,k,0,pflag)
        else:
            pass
           
    else:
        pass

    k+=1
    

# end of main analyze loop        
    
if k >= test_limit and test_limit > 0:
    g.printer('loop stopped due to test_limit',pflag)
else:
    pass

# saves the ana_file 
d.ana_file_saver(data_path,d.ana_file,1,'space',1,pflag)
g.printer('ana_file list finished',1)
print tm.time()-tstart
# 
# 
# 

    
