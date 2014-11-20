'''
Created on 29 Sep 2014

@author: ostein
'''
import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import shutil as st
import pickle 
from time import strftime, localtime
import time
import glob

# from list_class import lists
# from csv_list_class import csv_list


# c = csv_list()
# li = lists()

class gen():
    
    # Prints string as follows
    # Used at beginning of every function
    def tprinter(self,string,flag):
        if flag == 1: 
            print ''
            print '--------------------------------------------------------------'
            print str(string)
            print '--------------------------------------------------------------'
            print ''
        else:
            pass
    # simple print function     
    def printer(self,string,flag):
        if flag == 1: 
            print str(string)
            print ''
        else:
            pass

    def loop_info(self,i,maxi,flag):
        if flag == 1: 
            print ''
            print '=============================================================='
            print 'start analysing file nr. '+str(i)+' of '+str(maxi)
            print '=============================================================='
            print ''
        else:
            pass