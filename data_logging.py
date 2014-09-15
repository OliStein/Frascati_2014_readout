'''
Created on 8 Sep 2014

@author: ostein
'''
 def log_file_set(path,name):
        if not os.path.exists(str(path)+'\\log_files'):
            os.mkdir(str(path)+'\\log_files')
        
        # Directory of the script 
        self.c_dir = os.getcwd()
        
        # Create time string
        self.creat_time = strftime("%Y%m%d_%H%M", localtime())
        
        # Path and name of the log file
        self.log_file_path=path+'\\log_files\\'+str(name)+'_'+self.creat_time+'.txt'
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
    def log_path():
        return self.log_file_path

    def log_file_cleaner(path):
        for fl in glob.glob(str(path)+'\\log*.txt'):
            os.remove(fl)