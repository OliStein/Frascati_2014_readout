'''
Created on 18 Sep 2014

@author: ostein
'''

# Import of libraries 
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

# Class for printing text
# flag decides if printed or not

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

g = gen()
        
class csv_list():
    
    def csv_file_loader(self,path,fname,pflag):
        g.printer('running csv_file_loader',pflag)

        # Checks in path for fname 
        if os.path.isfile(os.path.join(path,fname)):
            g.printer(fname+' found',pflag)
            
            # Loads fname and writes it into data
            data = []
            with open(os.path.join(path,fname),'r') as f:
                for line in csv.reader(f,delimiter = ',', skipinitialspace = True):
                    data.append(line)
            f.close()
            self
           
        else:
            g.printer('no '+fname+' found',pflag)
           
       
        
        print ''
        return data       
    
    # Saves data_list to fname in path as .csv
    # flag indicates if existing file will be overwritten 
    def csv_file_safer(self,path,fname,data_list,flag,pflag):
        g.printer('running csv_file_safer',pflag)
        
        
         

        if os.path.isfile(os.path.join(path,fname)):

            g.printer(fname+' existing',pflag)
        
            if flag == 1:
                g.printer('file will be overwritten '+fname,pflag)
                   
            
                with open(os.path.join(path,fname),'wb') as f:
                    writer = csv.writer(f)
                    writer.writerows(data_list)
                f.close()
            else:
                g.printer('no writing',pflag)
           
        else:
            g.printer(fname+' not existing',pflag)
            g.printer('writing to '+fname,pflag)

           
            with open(os.path.join(path,fname),'wb') as f:
                writer = csv.writer(f)
                writer.writerows(data_list)
            f.close()
       
        
        print ''
        
class lists():
    def find_val(self,cname,lists,pflag):
        g.tprinter('running find_val',pflag)
        ind = lists.index(cname)
        g.printer('searched string '+str(cname),pflag)
        g.printer('position of '+str(cname)+' is '+str(ind),pflag)
        return ind
    
    def data_grabber(self,i,header,channel,pflag):
        g.tprinter('running data_grabber',pflag)
        
        pos = self.find_val('file',header,0)
        
        file_name = os.path.split(i[pos])[-1]
        file_path = os.path.split(i[pos])[0]
        g.printer(file_name,pflag)
        g.printer(file_path,pflag)
        
        return [file_path,file_name]
         
        
        
        
        
        
        
    
    
    
    
