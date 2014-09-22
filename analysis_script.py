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

l = log_files()
d = data()

li = lists()

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



header = d.ana_file[0]
k = 1
for i in d.ana_file[1:]:
    if k <= 20 and i >= len(d.ana_file): 
        
        li.data_grabber(i,header,3,1)
        print k
        
    else:
        print 'stop'
        break
    k += 1
    
# 
# 
# 
# d.ana_file_safer(data_path,d.ana_file,1,'bla',1,0)

# print int(d.ana_list[1][0])
# print d.ana_list[1][0]+1

# d.csv_file_safer(data_path,'test.csv',[[0,1,2,3,4,5,6]],1,0)
    