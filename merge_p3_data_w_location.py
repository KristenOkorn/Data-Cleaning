# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:55:11 2023

@author: kokorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd
from datetime import datetime, timedelta

#create a directory path for us to pull from / save to
path = 'C:\\Users\\kokorn\\Documents\\FRAPPE\\'

#files to loop through
file = ['CAMS','location']

#loop through each file to load in

for i in range(len(file)):

    #get the filename to be loaded
    filename = "P3_{}.csv".format(file[i])
    #combine the paths with the filenames for each
    filepath = os.path.join(path, filename)
    
    #load in the file
    if i == 0:
        CAMS = pd.read_csv(filepath)
        CAMS = CAMS.set_index('datetime')
    else:
        location = pd.read_csv(filepath)
        location = location.set_index('datetime')
        

#merge the two dataframes together
merge = pd.merge(location, CAMS, left_index=True, right_index=True)

#remove any NaNs
merge = merge.dropna()

#save out the final data
savePath = os.path.join(path,'P3_CAMS_location.csv')
merge.to_csv(savePath)