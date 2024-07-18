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

fileList = ['discoveraq-gascriteria_GROUND-NREL-GOLDEN_20140715_R0_thru20140812.ict']
#filelist = ['FRAPPE_CO','FRAPPE_NO2','FRAPPE_O3']

#loop through each file
for i in range(len(fileList)):

    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
 
    #load in the file
    temp = pd.read_csv(filePath,skiprows=52,header=0)
    
    #fix the HMS times
    temp[' start_sec-UTC'] = [timedelta(seconds=t) for t in temp[' start_sec-UTC']]
    
    #fix the fractional Julien times (day of year + hour)
    temp[' start_DOY-UTC'] = [pd.to_datetime(j, format='%j') for j in temp[' start_DOY-UTC']]

    #get the correct datetime strings together
    temp['month'] = [t.month for t in temp[' start_DOY-UTC']]
    temp['day'] = [t.day for t in temp[' start_DOY-UTC']]
    
    #combine all date strings
    temp['datetime'] = [datetime(2014, temp['month'][t], temp['day'][t]) for t in range(len(temp))]
    temp['datetime'] = temp['datetime'] + temp[' start_sec-UTC']

    #get just the columns we need
    gascrit = pd.DataFrame().assign(datetime = temp['datetime'], O3 = temp[' Ozone_ppbv'], NO2 = temp[' T500_NO2_ppbv'], SO2 = temp[' SO2_ppbv'])
   
    #save out to csv
    savePath = os.path.join(path,'gascrit.csv')
    gascrit.to_csv(savePath,index=False)