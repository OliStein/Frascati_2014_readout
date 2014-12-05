import os as os
import numpy as np
import time as tm


wdir = 'C:\\fd\\raw_data\\067_vs_02_27112014_L2_500_042690_021510_1_keithl_00_1500_1_00_1_500_0000_0000_0000_0000_0000_0000_0000_0000'


nfiles = 0
for file in os.listdir(wdir):
    print 'Checking file '+ file
    if file.endswith('.csv'):
        nfiles = nfiles+1


        #### READ AND PROPAGATE GLOBAL CHANGES TO FILE
        fin = open(wdir+'\\'+file, 'r')
        arr = []
        for line in fin.readlines():
            #split and join, to add the comma. This will remove the whitespace, but it should be ok. 
            linelist = line.split(':')
            arr.append(':,'.join(linelist))

        #### SAVE AND APPLY THE EXTRA COLUMN
        fnout = file

        fout = open(wdir+'\\output\\'+fnout, 'w')
        #Write first line of header

        fout.writelines(',Channel 4,Channel 2\n')

        #write unchanged header
        for i in arr[0:16]:
            fout.writelines(i)
            
        #Write DATE
        date = arr[16].strip('\n')
        date = date+','+date[-11:]+'\n'
        #print date
        fout.writelines(date)

        #Write timestamp
        time = arr[17].strip('\n').split(':,')
        timeOut = ':'.join([str(int(time[1])), str(int(time[2])), str(int(round(float(time[3]))))])
        ti = tm.strptime(timeOut, '%H:%M:%S')
        timeString = tm.strftime('%H:%M:%S', ti)
        #print time
        #print ti
        #print timeString
        OutString = 'Time:   ,'+timeString+','+timeString+'\n'
        fout.writelines(OutString)

        #Continue writing unchanged header
        for i in arr[18:20]:
            fout.writelines(i)
        #Write channel-list
        fout.writelines('Time Tags (Channel 4),Channel 4,Channel 2\n')
        #Write the datafile
        for i in arr[21:]:
            fout.writelines(i.strip('\n')+',0.0E0\n')
        fout.close()
        #tm.sleep(0.01)
    #tm.sleep(0.3)
    
    
fin.close()

print str(nfiles)+' files was changed.'
#print arr
print len(arr)