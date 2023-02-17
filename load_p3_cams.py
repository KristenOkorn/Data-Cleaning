# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 11:53:49 2023

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
for i in range(len(fileList)-1):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])

    #load in the file
    temp = pd.read_csv(filePath,skiprows=279,usecols = ['CH2O_Start_SOD_UTC',' CH2O_pptv'])
    
    #fix the HMS times temp = pd.read_csv(filePath temp = pd.read_csv(filePath
    temp['UTC_start'] = [timedelta(seconds=t) for t in temp['CH2O_Start_SOD_UTC']]
    
    #rename the HCHO column
    temp = temp.rename(columns={' CH2O_pptv': 'HCHO'})
    
    #now get the original datestamp to add to the time
    with open(filePath, 'r') as f:
        lines = f.readlines()
        date = lines[6]
        
    #remove the second date in here
    date = date[:-14]
        
    #now reforrmat as a datetime
    date = datetime.strptime(date, "%Y, %m, %d")
    
    #add this to our times of day
    temp['datetime'] = temp['UTC_start'] + date
    
    #get rid of what we don't need
    temp = temp.drop(columns=['CH2O_Start_SOD_UTC', 'UTC_start'])
    
    #make the datetimes the index
    temp = temp.set_index('datetime')
    
    #Save this into our full dataframe
    data = data.append(temp)
    

#resample (retime) the data to minutely
data = data.resample('T').mean()

#save out the final data
savePath = os.path.join(path,'P3_CAMS.csv')
data.to_csv(savePath)
