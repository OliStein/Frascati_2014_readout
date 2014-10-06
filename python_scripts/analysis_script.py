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

from csv_list_class import csv_list
from gen_class import gen
from data_manipulation import data_selector
from data_manipulation import data_math


l = log_files()
d = data()
c = csv_list()
# li = lists()
g = gen()
cwd = '/Users/Oli/work/Frascati/Frascati_2014_readout'
sel = data_selector()
m  = data_math() 

data_path = os.path.join(cwd,'data')
d.folder_check_create(data_path,0)
 
 
l.log_file_set(data_path,'log')
  
f = open(l.log_path(),'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)
  
  
d.check_infra_structure(data_path,1)
d.test_data_creator(data_path,1)
d.find_data(data_path,1)
# d.ana_file_creator(data_path,1)



# d.ana_file_deleter(data_path,1)

d.ana_file_loader(data_path,1)
d.ana_file_loader(data_path,1)
d.ana_file_sync(1) 

d.ana_file_checker(1)
print len(d.ana_file)
d.ana_file_saver(data_path,d.ana_file,1,'bla',1,1)

# Stop here
# sys.exit('stop')

# creates the header with the colum names
header = d.ana_file[0]


# set to one if all files to be analyzed
analyze_all = 0

# checks the number of files to be analyzed
naf = c.tba(d.ana_file,analyze_all,1)
# sets the limit of files to be analyzed
test_limit = 1

# iterator for 
k = 1

# save interval 
save_int = 10



# Stop here
# sys.exit('stop')





#main analysis loop
for i in d.ana_file[1:]:
    # conditions for analyzing the files
    # k is iterator and is limited by test_limit
    # if the file is already analyzed and the flag analyze all is not set, 
    # then only unanalyzed files will be treated
    if (k <= test_limit or test_limit < 0) and (i[c.find_val('analyzed',header,0)]!=1 or analyze_all == 1):
        # gives info of the actual file to be analyzed
        g.loop_info(k,naf,1)
        # gives name of file to be analyzed
        g.printer('File to be analyzed:',1) 
        g.printer(os.path.split(i[c.find_val('file',header,0)])[-1],1)
        
        # loads the data file
        data_comp = c.data_grabber(i,header,3,1)
        
        # splits the data in head list and data list
        data_head = data_comp[:22]
        data_header = data_head[-1]
        
        # converts data list into a numpy array 
        # last row will be ignored  
        data = np.array(data_comp[23:-1]).astype(float)
        
        # gives the data to data_manipulation class
        m.data_in(data,0)

        

#         m.data_plotter('icdBLM',1)
#         i[c.find_val('dBLM max. sig.',header,0)] = m.max_finder('idBLM',1)
        
        det_list = ['icBLM','dBLM','WC']
        for det in det_list:
            coln = sel.selector(det,1)
            g.printer(data_header[coln],1)
            if m.max_finder(det,coln,1) <= 2*abs(m.min_finder(det,coln,1)):
                m.inverter(det,coln,1)
            else:
                pass
            i[c.find_val(det+' max. sig.',header,0)] = m.max_finder(det,coln,1)
            i[c.find_val(det+' offset',header,0)] = m.offset_corr(det,coln,1)
            i[c.find_val(det+' noise',header,0)] = m.noise_finder(det,coln,1)
            
            m.data_plotter(det,coln,1)
            
        


#         g.printer(len(m.data),1)
#         
#         m.data_plotter('WC',1)
#         m.offset_corr('Wc',1)
# #         g.printer(sel.selector('icBLM',0),1)
#         m.data_plotter('WC',1)
        # prints max values of the data
#         g.printer(m.max_finder('WC',1),1)
#         g.printer(m.max_finder('icBLM',1),1)
#         g.printer(m.max_finder('dBLM',1),1)
#         m.data_plotter('dBLM',1)
#         m.inverter('dBLM',1)
#         m.data_plotter('dBLM',1)
#         g.printer(np.amin(data[:,sel.selector('a',0)]),1)
        
#         g.printer(max(data[:,sel.selector('dBLM')]),1)
        
        
        
        
        # data list which is saved in ana_data
        data_out = np.concatenate((np.array([data_head[-1]]),m.data),axis = 0)
        

        
        # sets the marker in the ana_file list to analyzed
        i[c.find_val('analyzed',header,0)] =1


        k += 1
#         print data_head

        # saves the ana_file for backup 
        if k % save_int == 0:
            d.ana_file_saver(data_path,d.ana_file,1,k,0,1)
        else:
            pass
        
        c.analyzed_save(header,data_out,i,1)
        # saves the ana_file 
        
    else:
        pass
    
    

# end of main analyze loop        
    
if k >= test_limit and test_limit > 0:
    g.printer('loop stopped due to test_limit',1)
else:
    pass

# saves the ana_file 
d.ana_file_saver(data_path,d.ana_file,1,'bla',1,1)
g.printer('ana_file list finished',1)
# 
# 
# 

    