# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:49:21 2022

@author: okorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd
from datetime import datetime, timedelta

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]

#create a dictionary to hold our data from each file
data_dict = {}

  
#iterate over each file in the main folder
for i in range(len(fileList)-1):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #load in the file
    temp = pd.read_csv(filePath,skiprows=35,usecols=['Timestamp','Concentration'])
    
    #Save this into our data dictionary
    data_dict['{}'.format(fileList[i])] = temp
    
#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#resample (retime) the data to minutely
full_data['Timestamp'] = pd.to_datetime(full_data['Timestamp'])
full_data = full_data.set_index('Timestamp').resample('1Min').ffill()

#Correct the datetime to the real time (not 1970)
start_time = datetime(2022,7,19,23,15,0) #guess a start time
timestamp = full_data.index[0]
time_delta = start_time - timestamp.to_pydatetime() #calculate the difference
#add the difference to each timestamp in our dataframe
full_data.index = full_data.index + time_delta

#rename the columns
full_data = full_data.rename(columns={"Concentration": "NO2"})
full_data.index.names = ['datetime']

#get the final data in a convenient format & remove negatives
NO2 = full_data
NO2 = NO2[(NO2['NO2']>0)]

#save out the final data
savePath = os.path.join(path,'NO2.csv')
NO2.to_csv(savePath)
