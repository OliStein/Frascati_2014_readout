#! c:\Python27\python
'''
Created on Nov 18, 2014

@author: Oli
'''
import sys
import os
import numpy as np


#--------------------------------------------------
# Important variables 
#--------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------------------------------------------
# PATH OF THE ROOT DIRECTORY
#--------------------------------------------------

# Oliver's mac path
cwd = '/Users/Oli/work/Frascati/Frascati_2014_readout'

# CHristian's PC path
# cwd = '/home/csoerens/Desktop/python/Frascati_Data_Analysis'

# cwd = 'C:\\Github'

# FLorian's mac path

# Daniel's mac path

# Labor Laptop path
# cwd = 'C:\\frascati_data'


sys.path.append(os.path.join(cwd,'python_scripts/sub_scripts'))

#--------------------------------------------------
# Importing custom made modules from sub_scripts
#--------------------------------------------------

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
cwd = '/Users/Oli/work/Frascati/Frascati_2014_readout'

# CHristian's PC path
# cwd = '/home/csoerens/Desktop/python/Frascati_Data_Analysis'

# cwd = 'C:\\Github'

# FLorian's mac path

# Daniel's mac path

# Labor Laptop path
# cwd = 'C:\\frascati_data'

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
# d.find_data(data_path,pflag)
# d.ana_file_creator(data_path,1)
