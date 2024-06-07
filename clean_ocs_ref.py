# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 16:13:05 2022

@author: okorn

Code will automatically ignore the string at the top
Need to manually delete the rows of strings at the bottom of each txt file
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
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #load in the file
    temp = pd.read_csv(filePath,skiprows=1,usecols=['                     Time','   [CO_dry]_ppm'])
 
    #remove empty spaces in data for workability
    temp.columns = temp.columns.str.strip()
    
    #remove any nans
    temp = temp.dropna()

    #Save this into our data dictionary
    data_dict['{}'.format(fileList[i])] = temp
    
#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#strip leading and trailing spaces
full_data['Time'] = full_data['Time'].str.strip()
#make our data a datetime
full_data['Time'] = pd.to_datetime(full_data['Time'],format= '%m/%d/%Y %H:%M:%S.%f')
#drop fractional seconds
full_data['Time'] = full_data['Time'].dt.floor('S')
#make time our index & ensure they're in increasing order
full_data = full_data.set_index('Time').sort_index()
#delete any messed up values
full_data = full_data[full_data.index.year >= 2023]
#convert our columns to numeric
full_data['[CO_dry]_ppm'] = pd.to_numeric(full_data['[CO_dry]_ppm'], errors='coerce')
#resample the data to minutely
full_data = full_data.resample('T').mean()

#get the final data in a convenient format
full_data = full_data.rename(columns={'Time':'datetime','[CO_dry]_ppm': 'CO'})
CO = pd.DataFrame(full_data['CO'], index=full_data.index)

#apply the calibration & convert to ppm from ppb
CO['CO'] = (CO['CO'] + 0.0134) * 997.5

#save out the final data
savePath = os.path.join(path,'CO.csv')
CO.to_csv(savePath)
