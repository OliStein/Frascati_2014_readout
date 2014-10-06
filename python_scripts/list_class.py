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

from gen_class import gen

g = gen()

# from csv_list_class import csv_list
# 
# c = csv_list()


class lists():
    def find_val(self,cname,lists,pflag):
        g.tprinter('running find_val',pflag)
        ind = lists.index(cname)
        g.printer('searched string '+str(cname),pflag)
        g.printer('position of '+str(cname)+' is '+str(ind),pflag)
        return ind
    
#     def data_grabber(self,i,header,channel,pflag):
#         g.tprinter('running data_grabber',pflag)
#         
#         pos = self.find_val('file',header,0)
#         
#         file_name = os.path.split(i[pos])[-1]
#         file_path = os.path.split(i[pos])[0]
#         g.printer(file_name,0)
#         g.printer(file_path,0)
#         try:
#             data_comp = c.csv_file_loader(file_path,file_name,0)
#             g.printer('data file successfully loaded',1)
#         except:
#             g.printer('no file loaded',1)
#         return data_comp         
        
    def tba(self,ana_file,analyze_all):
        g.tprinter('running tba',1)
        header = ana_file[0]
        naf = 0
        if analyze_all == 1:
            g.printer('analyze all files',1)
        else:
            pass
        for i in ana_file[1:]:
            if int(i[self.find_val('analyzed',header,0)])!=1 or analyze_all == 1:
                naf +=1
            else:
                pass
        
        g.printer(str(naf)+' of '+str(len(ana_file)-1)+' data sets have to be analyzed',1)
        
        return naf