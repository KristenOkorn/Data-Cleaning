# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:32:21 2023

@author: kokorn
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
data = pd.DataFrame()

#loop through each of the files & extract only the columns we need:
  #datetime, CO2 (wet), CH4 (wet), H2O
  
#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])

    #load in the file
    temp = pd.read_csv(filePath,skiprows=65,usecols = ['UTC',' FMS_ALT_PRES',' FMS_LAT',' FMS_LON'])
    
    #fix the HMS times
    temp['UTC'] = [timedelta(seconds=t) for t in temp['UTC']]
    
    #now get the original datestamp to add to the time
    with open(filePath, 'r') as f:
        lines = f.readlines()
        date = lines[6]
        
    #remove the second date in here
    date = date[:-17]
        
    #now reforrmat as a datetime
    date = datetime.strptime(date, "%Y, %m, %d")
    
    #add this to our times of day
    temp['datetime'] = temp['UTC'] + date
    
    #get rid of what we don't need
    temp = temp.drop(columns=['UTC'])
    
    #rename the columns
    temp = temp.rename(columns={' FMS_ALT_PRES':'Altitude',' FMS_LAT': 'Latitude',' FMS_LON':'Longitude'})
    
    #make the datetimes the index
    temp = temp.set_index('datetime')
    
    #Save this into our full dataframe
    data = data.append(temp)
    

#resample (retime) the data to minutely
data = data.resample('T').mean()

#save out the final data
savePath = os.path.join(path,'P3_location.csv')
data.to_csv(savePath)
