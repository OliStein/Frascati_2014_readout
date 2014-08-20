#! c:\Python27\python
'''
Created on 19 Aug 2014

@author: ostein
'''


from analysis_modules import log_files
from analysis_modules import data_move
from analysis_modules import Tee
import sys

data_path = 'C:\\work\\Frascati_2014\\New_readout_script\\data'


l = log_files()
dm = data_move()


l.log_file_set(data_path,'log')

f = open(l.log_path(),'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)


dm.check_infra_structure(data_path)
print "Hallo"