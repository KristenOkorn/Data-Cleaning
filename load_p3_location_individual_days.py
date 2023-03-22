# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:16:41 2023

Load from P3 AVOCET data

@author: okorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd
from datetime import datetime, timedelta

#Prompt user to select folder for analysis - P3B Avocet has lat lon alt
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]


#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])

    #load in the file
    temp = pd.read_csv(filePath,skiprows=36,usecols = ['UTC',' Lat', ' Lon', ' Alt'])
    
    #fix the HMS times
    temp['UTC'] = [timedelta(seconds=t) for t in temp['UTC']]
    
    #get the date string to use when we save it out
    date_str=fileList[i][19:27]
        
    #now reforrmat as a datetime
    date = datetime.strptime(date_str, "%Y%m%d")
    
    #add this to our times of day
    temp['datetime'] = temp['UTC'] + date
    
    #get rid of what we don't need
    temp = temp.drop(columns=['UTC'])
    
    #rename the columns
    temp = temp.rename(columns={' Lat' :'Latitude',' Lon': 'Longitude',' Alt' :'Altitude'})
    
    #make the datetimes the index
    temp = temp.set_index('datetime')
    
    #resample (retime) the data to minutely
    temp = temp.resample('T').mean()

    #save out the final data
    savePath = os.path.join(path,'{}_P3_location.csv'.format(date_str))
    temp.to_csv(savePath)
