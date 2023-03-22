# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:57:27 2023

Load in the P3 CAMS data

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
data = pd.DataFrame()

  
#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #get the number of rows to skip
    nskip = pd.read_csv(filePath, nrows=0)
    nskip = int(nskip.columns[0])

    #load in the file
    temp = pd.read_csv(filePath,skiprows=nskip-1,usecols = ['CH2O_Start_SOD_UTC',' CH2O_pptv'])
    
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
    
    #resample (retime) the data to minutely
    temp = temp.resample('T').mean()
    
    #get the date string to use when we save it out
    date_str=fileList[i][20:28]

    #save out the final data
    savePath = os.path.join(path,'{}_CAMS.csv'.format(date_str))
    data.to_csv(savePath)