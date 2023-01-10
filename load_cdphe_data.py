# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:59:07 2023

@author: kokorn
"""

# import libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from tkinter.filedialog import askdirectory

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

fileList = ['CDPHE.ICT']
#filelist = ['FRAPPE_CO','FRAPPE_NO2','FRAPPE_O3']

#loop through each file
for i in range(len(fileList)):

    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
 
    #load in the file
    temp = pd.read_csv(filePath,skiprows=46,header=0)
    
    #fix the HMS times
    temp['UTC_start'] = [timedelta(seconds=t) for t in temp['UTC_start']]
    
    #fix the fractional Julien times (day of year + hour)
    temp['FJD'] = [pd.to_datetime(j, format='%j') for j in temp['FJD']]

    #get the correct datetime strings together
    temp['month'] = [t.month for t in temp['FJD']]
    temp['day'] = [t.day for t in temp['FJD']]
    
    #combine all date strings
    temp['datetime'] = [datetime(temp['year'][t], temp['month'][t], temp['day'][t]) for t in range(len(temp))]
    temp['datetime'] = temp['datetime'] + temp['UTC_start']

    #get just the columns we need
    CDPHE = pd.DataFrame().assign(datetime = temp['datetime'], O3 = temp['Ozone'], NO2 = temp['NO2'], CO = temp['CO'])
   
    #save out to csv
    savePath = os.path.join(path,'CDPHE.csv')
    CDPHE.to_csv(savePath,index=False)