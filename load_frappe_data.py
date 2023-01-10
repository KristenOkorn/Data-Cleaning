# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:18:10 2023

@author: kokorn
"""

# import libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from tkinter.filedialog import askdirectory
import linecache

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#fileList = ['CDPHE.ICT']
fileList = ['FRAPPE_CO','FRAPPE_NO2','FRAPPE_O3']

#loop through each file
for i in range(len(fileList)):

    #add file extension
    fullFile = fileList[i] + '.ict'
    
    #Create full file path for reading file
    filePath = os.path.join(path, fullFile)
 
    #load in the file
    temp = pd.read_csv(filePath,skiprows=34,header=0)
    
    #get the start date
    date = linecache.getline(filePath, 7)
    #get it alone
    date = date[:-15]
    #get in datetime format
    sep = date.split(',')
    date = datetime(int(sep[0]),int(sep[1]),int(sep[2]))
    
    #combine the elapsed seconds with the start datetime
    temp['datetime'] = [date + timedelta(seconds=t) for t in temp['Start_UTC']]

    #get just the columns we need
    temp = temp.drop(columns=['Start_UTC', ' Stop_UTC', ' Mid_UTC'])
    #reorder so datetime is first
    temp = temp.iloc[:,[1,0]]
    
    #save out to csv
    savePath = os.path.join(path,'{}.csv'.format(fileList[i]))
    temp.to_csv(savePath,index=False)