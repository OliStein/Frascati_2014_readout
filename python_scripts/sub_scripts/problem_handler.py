'''
Created on Dec 11, 2014

@author: Oli

'''
# from analysis_modules import log_files
# from analysis_modules import data
# from analysis_modules import Tee
# import matplotlib.pyplot as plt

# from csv_list_class import csv_list
# from gen_class import gen
# from data_manipulation import data_selector
# from data_manipulation import data_math
# import time as tm
import numpy as np

# l = log_files()
# d = data()
# c = csv_list()
# li = lists()
# g = gen()


# Class for problem handling


class prob_handler():
    
#     def __init__(self):
#         self.prob_flag = 0

        
    def header_print(self):
        return prob_header

        
    def list_num(self,i):
        self.num = i

    def flag_set(self):
        self.prob_flag = 1

    def ana_file_set(self,info):
        self.info = info
        if self.prob_flag != 0:  
            self.num[np.where(self.header == 'problem')[0][0]] = self.info
#             = self.info
        else:
            self.num[np.where(self.header == 'problem')[0][0]] = self.info
#             = 'no'
        print self.num[np.where(self.header == 'problem')[0][0]]
    def flag_ret(self):
        return self.prob_flag
    
    def info_ret(self):
        return self.info
#     def problem_init(self):
#         self.prob = 'no' 
#         
#     def problem_check(self):
#         if self.prob != 'no':
#              return break 
#         
#     def problem_flag_set(self,set,header):
#         self.prob = set
#         self.problem_check()   