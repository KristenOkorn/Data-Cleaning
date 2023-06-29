# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:47:57 2023
Note that this data has already been edited in excel to correct datetime
(instrument was 6 min fast & was d/m/y instead of m/d/y)
and also already did linear correction factor based on o3 generator calibration
@author: kokorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Create full file path for reading file
filePath = os.path.join(path, 'Calibrated data - full data.csv')
    
#load in the file
temp = pd.read_csv(filePath,usecols=['corrected_datetime','corrected_o3'])

# Resample the DataFrame to minute frequency and calculate the mean value
temp = temp.resample('T').mean()

# Rename the column using the rename() function
temp = temp.rename(columns={'corrected_datetime': 'datetime'})
temp = temp.rename(columns={'corrected_o3': 'O3'})

#save out a csv to use as reference data
savePath = os.path.join(path,'O3_may23.csv')
temp.to_csv(savePath)