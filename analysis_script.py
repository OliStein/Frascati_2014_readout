#! c:\Python27\python
'''
Created on 19 Aug 2014

@author: ostein
'''


from analysis_modules import log_files
from analysis_modules import data
from analysis_modules import Tee
import sys

data_path = 'C:\\work\\Frascati_2014\\New_readout_script\\data'


l = log_files()
d = data()


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




d.ana_file_safer(data_path,d.ana_file,1,1,0,'bla')

# print int(d.ana_list[1][0])
# print d.ana_list[1][0]+1

# d.csv_file_safer(data_path,'test.csv',[[0,1,2,3,4,5,6]],1,0)
    