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

class data_selector():
    def selector(self,detector,data_header):
        
        out = 0
        if detector == 'dBLM':
            out = 1
        elif detector == 'icBLM':
            out = 2
        elif detector == 'WC':
            out = 3
        return out
