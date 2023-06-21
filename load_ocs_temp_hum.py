# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 09:16:15 2022

@author: okorn

Just to get temperature and pressure for comparing with CAPS NO2 instrument
"""


#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd
import datetime

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]

#create a dictionary to hold our data from each file
data_dict = {}

#loop through each of the files & extract only the columns we need:
  #datetime, CO (dry)
  
#iterate over each file in the main folder
for i in range(len(fileList)-1):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #load in the file
    temp = pd.read_csv(filePath,skiprows=1,usecols=['                     Time','      GasP_torr','         AmbT_C'])
 
    #remove empty spaces in data for workability
    temp.columns = temp.columns.str.strip()

    #Save this into our data dictionary
    data_dict['{}'.format(fileList[i])] = temp
    
#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#make our data a datetime
full_data['Time'] = pd.to_datetime(full_data['Time'])
#delete any measurements less than a second apart
full_data = full_data.drop_duplicates(subset='Time')
#make time our index & ensure they're in increasing order
full_data = full_data.set_index('Time').sort_index()
#resample (retime) the data to minutely
full_data = full_data.resample('T').mean()

#save out the final data
savePath = os.path.join(path,'ocs_temp_hum.csv')
full_data.to_csv(savePath)
