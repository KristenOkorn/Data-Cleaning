# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:34:05 2023

Merge individual days of P3 data - CAMS and location from AVOCET
@author: okorn
"""

#Import in necessary packages
import os
import pandas as pd

#create a directory path for us to pull from / save to
path = 'C:\\Users\\okorn\\Documents\\FRAPPE\\P3B CAMS'
camspath = 'C:\\Users\\okorn\\Documents\\FRAPPE\\P3B CAMS\\CAMS'
locpath = 'C:\\Users\\okorn\\Documents\\FRAPPE\\P3B CAMS\\location'

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(camspath) if isfile(join(camspath, f))]

#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(camspath, fileList[i])
    
    #load in the file
    CAMS = pd.read_csv(filePath)
    
    #get the date string to use when we save it out
    date_str=fileList[i][0:8]
    
    #Get the path for the location data
    filePath = os.path.join(locpath, '{}_P3_location.csv'.format(date_str))
    
    #load in the location data matching this date
    location = pd.read_csv(filePath)
        
    #merge the two dataframes together
    merge = pd.merge(location, CAMS, left_index=True, right_index=True)

    #remove any NaNs
    merge = merge.dropna()

    #save out the final data
    savePath = os.path.join(path,'{}_CAMS_location.csv'.format(date_str))
    merge.to_csv(savePath)