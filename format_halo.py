# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:23:55 2023

@author: okorn

Load in h5 HALO column data
"""

#import libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from tkinter.filedialog import askdirectory
import h5py

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]

#create a dataframe to hold our data from each file
data = pd.DataFrame()

  
#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    f = h5py.File(filePath, 'r')
    
    #print the list of base items for our reference
    print(list(f.items()))
    
    #get the initial date from the filename
    year = fileList[i][24:28]
    month = fileList[i][28:30]
    day = fileList[i][30:32]
    date = datetime.strptime('{}-{}-{}'.format(year,month,day), "%Y-%m-%d")
   
    #unpack the methane data products layer
    ch4 = f.get('CH4DataProducts')
    #print(ch4.keys())
    #get the column data
    mlh = np.array(ch4.get('MixedLayerHeight'))
    xch4 = np.array(ch4.get('XCH4_clear'))
        
    #unpack the navigation layer
    nav = f.get('Nav_Data')
    #print(nav.keys())
    #get the nav data
    altitude = np.array(nav.get('gps_alt'))
    latitude = np.array(nav.get('gps_lat'))
    longitude = np.array(nav.get('gps_lon'))
    time = np.array(nav.get('gps_time'))
    
    #Convert decimal hours to hours, minutes, and seconds
    hours, remainder = divmod(time * 3600, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = np.round(seconds) #round seconds the nearest whole number
    
    #Convert to datetime array
    my_datetime = []
    for h, m, s in zip(hours.flat, minutes.flat, seconds.flat):
        delta = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        my_datetime.append(date + delta)    
    my_datetime = np.array(my_datetime)
        
    #save all the data we extracted as a dataframe
    df = pd.DataFrame(index=my_datetime)
    df['XCH4'] = xch4
    df['mlh'] = mlh
    df['latitude'] = latitude
    df['longitude'] = longitude
    df['altitude'] = altitude
  
    #close out of this file
    f.close()
    
    #concatenate data from this loop into the overall dataframe
    data = data.append(df)
     
#retime to minutely averages
data = data.resample('T').mean()

#drop NaN values
data = data.dropna()

#save out the final (raw) data
savePath = os.path.join(path,'HALO_XCH4.csv')
data.to_csv(savePath)