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
cwd = os.getcwd()
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
d.ana_file_creator(data_path,1,1)
d.ana_file_loader(data_path,1)
 
d.ana_file_checker(1)






# creates the header with the colum names
header = d.ana_file[0]


# set to one if all files to be analyzed
analyze_all = 1
# checks the number of files to be analyzed
naf = c.tba(d.ana_file,analyze_all)
# sets the limit of files to be analyzed
test_limit = 5
# iterator for 
k = 1

#main analysis loop
for i in d.ana_file[1:]:
    if (k <= test_limit or test_limit < 0) and (int(i[c.find_val('analyzed',header,0)])!=1 or analyze_all == 1):
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
        data = np.array(data_comp[23:-1]).astype(float)
        m.data_in(data,0)
#         m.data_plotter()
#         m.set_data_zero()
        
#         g.printer(m.data[:10],1)
 
#         i[c.find_val('dBLM max. sig.',header,0)] = max(data[:,(0,sel.selector['dBLM'])])
        
#         i[c.find_val('icBLM max. sig.',header,0)] = m.max_finder('icBLM',1)
        g.printer(m.max_finder('WC',1),1)
        g.printer(m.max_finder('icBLM',1),1)
        g.printer(m.max_finder('dBLM',1),1)
        m.data_plotter('dBLM',1)
        m.inverter('dBLM',1)
        m.data_plotter('dBLM',1)
        g.printer(np.amin(data[:,sel.selector('a',0)]),1)
        
#         g.printer(max(data[:,sel.selector('dBLM')]),1)
        
        
        
        
        # data list which is saved in ana_data
#         data_out = np.array([data_head[-1]])+data
        
#         g.printer(data_out,1)
        
        # sets the marker in the ana_file list to analyzed
        i[c.find_val('analyzed',header,0)] =1

        print i
        print k
        k += 1
#         print data_head
#         c.analyzed_save(header,data_out,i,1)
    else:
        pass

# end of main analyze loop        
    
if k >= test_limit:
    g.printer('loop stopped due to test_limit',1)
else:
    pass

# saves the ana_file 
d.ana_file_safer(data_path,d.ana_file,1,'bla',1,1)
g.printer('ana_file list finished',1)
# 
# 
# 

    