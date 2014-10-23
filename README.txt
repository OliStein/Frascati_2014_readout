Oliver Stein
oliver.sein@cern.ch



v1.0
15.09.2014

O. Stein

Analysis scripts for Frascati measurements

analysis_modules.py contains classes and functions for the analysis of the data files.
Specific informations can be found in the file.

analysis_script.py calls functions for the analysis of the data. Is the actual script working with the data.

Required structure:

#Working_folder
\\data
	\\raw_data
	\\ana_data
	\\log_files 

folder_batch.csv gives the list of measurement parameter which creates the folders for the data.


Opening and working the DataAnalysisExample.ipynb is done by navigating to the 
folder, opening a terminal and typing 'ipython notebook'. This should start an
interface in a browser, that enables fast prototyping and goodies!


 
