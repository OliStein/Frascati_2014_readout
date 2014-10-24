How to use the analysis files 

Required software:
git
python 2.7
	+ numpy
	+ matplotlib

1.
	check if python is installed
	terminal/console python
		Version info...
		>>>
		exit with ctrl+d

		check if numpy and matplotlib is installed
		terminal/console python
		>>> import numpy
		>>> import matplotlib	

	if not installed 
		install python 2.7
		install numpy
		install matplotlib
		(install pandas)

	it might be good to install the anaconda python distribution
	http://continuum.io/downloads
2.
	check if git is already installed:
		terminal/console
			git
	if not:		
		install git
		http://git-scm.com/
3. 
	create read_out_path where the read out file structure will be installed
		Example: /Users/Oli/work/Frascati
	
	download repository
		terminal/console 
			git clone https://github.com/OliStein/Frascati_2014_readout.git

			repeat once in a while:

			git pull https://github.com/OliStein/Frascati_2014_readout.git
	
	goto:read_out_path
		cd read_out_path
	goto:python_scripts
		cd Frascati_2014_readout
		cd python_scripts

4. edit python scripts
	open the files with editor
		sublime, vim, notepad++ etc. 

		needed modifications:
		in the beginning of analysis_script.py
		Add read_out_path to the specific user
		and comment the the other user path

		#--------------------------------------------------
		# PATH OF THE ROOT DIRECTORY
		#--------------------------------------------------

		# Oliver's mac path
		cwd = '/Users/Oli/work/Frascati/Frascati_2014_readout'

		# CHristian's PC path
		# cwd = '/home/csoerens/Desktop/python/Frascati_Data_Analysis'

		# cwd = 'C:\\Github'

		# FLorian's mac path
		needs to be added

		# Daniel's mac path
		needs to be added
		# Labor Laptop path
		needs to be added


5. execute python script
	python analysis_scripts 

	first run will create infrastructure 

	example data has to be copied into the /raw_data folder

	rerun script

	script should run through the data and analyze the example data sets


