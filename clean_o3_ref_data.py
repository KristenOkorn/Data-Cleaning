# -*- coding: utf-8 -*-
"""
Created on Mon May 20 23:44:03 2024

Load, calibrate, & reformat Ozone calibration data (2B Tech)

@author: okorn
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 22:01:15 2022

@author: okorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]

#create a dictionary to hold our data from each file
data_dict = {}

  
#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #load in the file
    temp = pd.read_csv(filePath,sep=',', header=None, usecols=[0,4,5],
                       names=['O3','date','time'])
    #drop NaNs
    temp = temp.dropna()
    #also drop the first line - doesn't always record
    temp = temp.drop(index=0)
    #combine date & time
    temp['datetime'] = pd.to_datetime(temp['date'] + ' ' + temp['time'])
    
    #Save this into our data dictionary
    data_dict['{}'.format(fileList[i])] = temp
    
#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#apply the calibration correction for O3
full_data['O3'] = (full_data['O3']*0.9704) + 4.6719

#make the datetime the index
full_data.index = full_data['datetime']
#drop the original datetime column
full_data.drop(['datetime'],axis=1,inplace=True)
#retime
full_data = full_data.resample("T").mean()

#remove empty rows from retime
full_data = full_data.dropna()

#Picarro runs 1 min and 2-3 sec slower - account for this
full_data.index = full_data.index + pd.Timedelta(minutes=7, seconds=2)

#save out the final data
savePath = os.path.join(path,'O3_2024.csv')
full_data.to_csv(savePath)
