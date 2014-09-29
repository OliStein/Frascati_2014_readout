#! c:\Python27\python
'''
Created on 19 Aug 2014

@author: ostein
'''


from analysis_modules import log_files
from analysis_modules import data
from analysis_modules import Tee
import sys
import os

from minions import lists
from minions import csv_list
from minions import gen


l = log_files()
d = data()
c = csv_list()
li = lists()
g = gen()
cwd = os.getcwd()

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
naf = li.tba(d.ana_file,analyze_all)
# sets the limit of files to be analyzed
test_limit = 5
# iterator for 
k = 1

#main analysis loop
for i in d.ana_file[1:]:
    if (k <= test_limit or test_limit < 0) and (int(i[li.find_val('analyzed',header,0)])!=1 or analyze_all == 1):
        # gives info of the actual file to be analyzed
        g.loop_info(k,naf,1)
        # gives name of file to be analyzed
        g.printer('File to be analyzed:',1) 
        g.printer(os.path.split(i[li.find_val('file',header,0)])[-1],1)
        
        # loads the data file
        data_comp = li.data_grabber(i,header,3,1)
        # splits the data in head list and data list
        data_head = data_comp[:22]
        data = data_comp[23:]
        
 
 
        
        
        
        
        # data list which is saved in ana_data
        data_out = [data_head[-1]]+data
        
#         g.printer(data_out,1)
        
        # sets the marker in the ana_file list to analyzed
        i[li.find_val('analyzed',header,0)] =1

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

    