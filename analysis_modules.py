#! c:\Python27\python
'''
Created on 19 Aug 2014

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


# Class for writing the console output in a log file
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            
# Class for printing text
#flag decides if printed or not
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
# Class for analysing the data
class log_files():
    
    # Setting up the log file in the directory where the script is saved
    def log_file_set(self,path,name):
        if not os.path.exists(os.path.join(path,'log_files')):
            os.mkdir(os.path.join(path,'log_files'))
        
        # Directory of the script 
        self.c_dir = os.getcwd()
        
        # Create time string
        self.creat_time = strftime("%Y%m%d_%H%M", localtime())
        
        # Path and name of the log file
        self.log_file_path=os.path.join(path,'log_files',str(name)+'_'+self.creat_time+'.txt')
        print self.log_file_path
        
        # Head of the log file
        print ''
        self.log_file=open(self.log_file_path,'w+')
        
        print >> self.log_file, '-------------------------------------------------------' 
        print >> self.log_file, 'Data analysis Log_file'
        print >> self.log_file, ''
        print >> self.log_file, 'Script_file dir: '+str(self.c_dir)
        print >> self.log_file, 'Log_file dir: '+str(path)
        print >> self.log_file, 'Log_file name: '+str(name)+'_'+self.creat_time+'.txt'
        print >> self.log_file, ''
        print >> self.log_file, 'date: '+strftime("%a, %d %b %Y", localtime())
        print >> self.log_file, 'time: '+strftime("%H:%M:%S", localtime())
        print >> self.log_file, ''
        print >> self.log_file, '-------------------------------------------------------'
#         print >> self.log_file, 'current directory: '+str(self.c_dir)
#         print >> self.log_file, 'root directory: '+str(self.start)
        print >> self.log_file, ''
#         print >> self.log_file, self.out
        print >> self.log_file, ''
    
        # Closing file
        self.log_file.close()
    
    # Returns the path of the log file
    def log_path(self):
        return self.log_file_path

    def log_file_cleaner(self, path):
        for fl in glob.glob(os.path.join(path,'log*.txt')):
            os.remove(fl)

class data():
    # Checks and creates folder at given path
    def folder_check_create(self,path,pflag):
        g.printer('checking',pflag)
        g.printer(path,pflag)
        
        if  os.path.exists(path):
            
            g.printer('path exists',pflag)
            
        else: 
            g.printer('path does NOT exists',pflag)
        
            os.mkdir(path)
            g.printer('path created',pflag)
           

        
    # Checking for infrastructure
    def check_infra_structure(self,path,pflag):
        g.tprinter('checking for infrastructure',pflag)
        
        # In \\raw_data the scope data will be stored 
        ndir = 'raw_data'
        npath = os.path.join(path,ndir)
        self.folder_check_create(npath,pflag)
        
        # In \\ana_data the analysed data will be stored
        ndir = 'ana_data'
        npath = os.path.join(path,ndir)
        self.folder_check_create(npath,pflag)
     
    # function for loading csv files in a list [[]]
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
            
        
        

    # function for creating folder with the right folder naming 
    def test_data_creator(self,path,pflag):
        g.tprinter('running test data creator',pflag)
        
        # Checks and creates the \\raw_data folder
        ndir='raw_data'
        npath=os.path.join(path,ndir)
        self.folder_check_create(npath,pflag)
        
        # If path exists csv-batch file will be loaded
        if os.path.exists(str(path)+str(ndir)):
            print ndir+' exists'
            
            # Loading .csv bath file
            # Writes the loaded file into list
            self.batch_data = self.csv_file_loader(path,'folder_batch.csv',0) 
            
            # Checks and creates a folder with name from self.batch_data list 
            for i in self.batch_data[1::]:
                nfolder = '_'.join(i)
                npath=os.path.join(path,ndir,nfolder)
                self.folder_check_create(npath,pflag)
                    
                
        else :
            pass
        
        print ''
        
    # Function for finding the data files in the \\raw_data path and writing the info to self.data_list
    def find_data(self,path,pflag):
        g.printer('running find_data',1)
        self.data_list = []
        for paths,dirs,files in os.walk(os.path.join(path,'raw_data')):
            
            for f in files:        
                self.data_list.append(os.path.join(paths,f))
        print ''
    # Creates an analysis file as .csv and saves it to path
    # This is the base for the analysis
    # The file will be loaded and completed with the analysis results  
    # Flag indicates if the existing file will be overwritten  
    def ana_file_creator(self,path,flag,pflag):
        g.tprinter('running ana_file_creator',pflag)
        ana_file = 'ana_file.csv'
        # HEader with the column names
        self.ana_list = [['id','meas. type','run','date','detector','type','xpos','ypos','icBLM','icBLM DAQ','att. icBLM','volt. icBLM','dBLM',
                          'att. DBLM','shunt','volt. dBLM','scpr11','scpr12','scpr21','scpr22','udc','meas. nr.','time',
                          'WC','WC sig.','WC noise','WC offset','WC max. sig.','WC FWHM','WC int','WC charge','WC ppb',
                          'icBLM','icBLM sig.','icBLM noise','icBLM offset','icBLM max. sig.','icBLM max sig. att. corr.','icBLM FWHM','icBLM int.','icBLM int. att. corr.','icBLM charge sig.','icBLM ppb',
                          'dBLM','dBLM sig.','dBLM noise','dBLM offset','dBLM max. sig.','dBLM max sig. att. corr.','dBLM FWHM','dBLM int.','dBLM int. att. corr.','dBLM charge sig.',
                          'analyzed','file']]
        # Extends the list with the found data files and pathes
        # Analysis results are set to zero in the beginning
        for i in self.data_list:
            k = os.path.split(i)
            info = k[-1].split('.')[-2].split('_')
#             info[0]= int(info[0])
#             info[3]= int(info[3])
#             info[5]= int(info[5])
            
#             print len(self.ana_list[0])
#             print [0]*(len(self.ana_list[0])-len(info))
            info = info+[0]*(len(self.ana_list[0])-len(info)-1)
            info.append(i)
            self.ana_list.append(info)
        
        
        
        # Saves the analysis file 
        if os.path.isfile(os.path.join(path,ana_file)):
            if flag == 1:
                g.printer(ana_file+' exists but will be overwritten',pflag)
#                 print ana_file+' exists but will be overwritten'
                
                
                self.csv_file_safer(path,ana_file,self.ana_list,flag,pflag)
                
#                 with open(os.path.join(path,ana_file),'wb') as f:
#                     writer = csv.writer(f)
#                     writer.writerows(self.ana_list)
#                 f.close()
            else:
                g.printer(ana_file+' exists',pflag)
#                 print ana_file+' exists'
        else:
            g.printer(ana_file+' does NOT exist',pflag)
#             print ana_file+' does NOT exist'
            self.csv_file_safer(path,ana_file,self.ana_list,1,0)
#             with open(os.path.join(path,ana_file),'wb') as f:
#                 writer = csv.writer(f)
#                 writer.writerows(self.ana_list)
#             f.close()
        print ''
        
    # Loads the analysis file    
    def ana_file_loader(self,path,pflag):
        g.tprinter('running ana_file_loader',pflag)
        
        self.ana_file = self.csv_file_loader(path,'ana_file.csv',1) 
        
#         return self.ana_file
    # Checks if the analysis file exists
    # If not program stops and gives error message
    def ana_file_checker(self,pflag):
        g.tprinter('running ana_file_checker',pflag)
        
        try:
            self.ana_file[0]
            self.ana_check = 1
            
               
        except:
            self.ana_check = 0
            self.ana_file = 0
            sys.exit('ana_file not a list or defined')
    
        if len(self.ana_file[0]) == 55:
            
            self.ana_check = 1
            
               
        else:
            self.ana_check = 0
            self.ana_file = 0
            sys.exit('ana_file not correct length')
        
        g.printer('ana_file ok',pflag)        
        
    # Saves analysis file 
    # flag for overwriting
    # sflag for saving as ana_file or ana_file_str(info)        
    def ana_file_safer(self,path,data_list,flag,info,sflag,pflag,):
    
        g.tprinter('running ana_file_safer',pflag)
        if sflag == 1:
            
            ana_file_name = 'ana_file.csv'
            g.printer('file name: '+ana_file_name,pflag)
        else:
            ana_file_name ='ana_file_'+str(info)+'.csv'
            g.printer('file name: '+ana_file_name,pflag)
        self.csv_file_safer(path,ana_file_name,data_list,flag,pflag)
   
        
        
        