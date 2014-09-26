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
d.ana_file_creator(data_path,0,1)
d.ana_file_loader(data_path,1)
 
d.ana_file_checker(1)





header = d.ana_file[0]






analyze_all = 1
naf = li.tba(d.ana_file,analyze_all)


k = 1
for i in d.ana_file[1:]:
    if k <= 20 and int(i[li.find_val('analyzed',header,0)])!=1 or analyze_all == 1:
        g.loop_info(k,naf,1)
        g.printer('File to be analyzed:',1) 
        g.printer(os.path.split(i[li.find_val('file',header,0)])[-1],1)
        
        data_comp = li.data_grabber(i,header,3,1)
        data_head = data_comp[:22]
        data = data_comp[23:]
        
        
        data_out = [data_head[-1]]+data[1:4]
        
        g.printer(data_out,1)
#         c.csv_file_safer()
        save_folder =  os.path.split(os.path.split(os.path.split(i[li.find_val('file',header,0)])[0])[-1])[-1]
        save_path = os.path.join(os.path.split(os.path.split(os.path.split(i[li.find_val('file',header,0)])[0])[0])[0],'ana_data')
        save_path_comp = os.path.join(save_path,save_folder)
        file_name ='analyzed'+os.path.split(i[li.find_val('file',header,0)])[-1]
        g.printer(save_path_comp,1)
        g.printer(file_name,1)
        c.csv_file_safer(save_path_comp,file_name,data_out,1,1)
#         g.printer(save_folder,1)
        
        k += 1
#         print data_head
    else:
        pass
        
    

g.printer('ana_file list finished',1)
# 
# 
# 
# d.ana_file_safer(data_path,d.ana_file,1,'bla',1,0)

# print int(d.ana_list[1][0])
# print d.ana_list[1][0]+1

# d.csv_file_safer(data_path,'test.csv',[[0,1,2,3,4,5,6]],1,0)
    