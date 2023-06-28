# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 10:12:51 2022

Load in CIT-AQS data

@author: okorn
"""

#Import helpful toolboxes etc.
import pandas as pd
import os
import numpy as np
from  datetime import datetime, timedelta

#create a directory path for us to pull from / save to
path = 'C:\\Users\\okorn\\Documents\\2022 Deployment\\CIT-AQS\\Data\\'

#get list of files to loop through
files = os.listdir(path)

#loop through each file to load in
for i in range(len(files)):

    #get the filename to be loaded
    filename = files[i]
    #combine the paths with the filenames for each
    filepath = os.path.join(path, filename)

    #load in the file
    aqs = pd.read_csv(filepath,skiprows=43,usecols=['UTC_Start',
           'CO_CIT_AQS', 'O3_CIT_AQS', 'NO2_CIT_AQS'])

    #get the date for this file
    #remove other strings from the filename
    date = filename.replace('LAAQC22-CIT-AQS_CITHALL_', '')
    date = date.replace('_RA.ict.txt', '')
    #get in datetime format
    date = datetime(int(date[:4]),int(date[5:6]),int(date[6:]))
    
    #convert from seconds past midnight to datetime
    time = np.array([date + timedelta(seconds = td) for td in aqs['UTC_Start']])
    
    #create a dataframe with the new data
    aqs2 = pd.DataFrame([time,aqs['CO_CIT_AQS'],aqs['O3_CIT_AQS'],aqs['NO2_CIT_AQS']]).transpose()
    
    #add names to dataframe columns
    aqs2.columns =['datetime', 'CO', 'O3', 'NO2']
    
    #if this is the first file, rename & resave
    if i == 0:
        df = aqs2
      
    #if this isn't the first file, append it to the rest
    else: 
        #append this data to the final dataframe
        df = df.append(aqs2)

#data cleaning - remove any -9999's
# df[df['CO'] < 0] = 'NaN'
# df[df['O3'] < 0] = 'NaN'
# df[df['NO2'] < 0] = 'NaN'

#save out the final data
savePath = os.path.join(path,'CIT_AQS.csv')
df.to_csv(savePath)