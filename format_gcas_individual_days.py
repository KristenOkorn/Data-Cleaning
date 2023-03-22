# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:30:17 2023

Load in h5 GCAS NO2 column data & save out as a minute average CSV
FOR EACH INDIVIDUAL DAY
@author: okorn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:19:26 2023

Load in h5 GCAS NO2 column data & save out as a minute average CSV

@author: kokorn
"""

# import libraries
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


#iterate over each file in the main folder
for i in range(len(fileList)):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    f = h5py.File(filePath, 'r')
    
    #print the list of base items for our reference
    print(list(f.items()))
    
    #different labeling systems may exist - try both
    
    if f.get('GEOLOCATION_PARAMETERS') is None:
        #must be lower case version - proceed
        geoloc = f.get('Geolocation')
        print(geoloc.keys())
        #get the parameters we need from this layer
        altitude = np.array(geoloc.get('AircraftAltitude')).T
        lat = np.array(geoloc.get('Latitude')).T
        lon = np.array(geoloc.get('Longitude')).T
        month = np.array(geoloc.get('Month')).T
        year = np.array(geoloc.get('Year')).T
        timestamp = np.array(geoloc.get('UTCHours')).T
        day = np.array(geoloc.get('Day')).T
        
        #reformat the date strings
        date = np.array([str(month[t]) + str(day[t]) + str(year[t]) for t in range(len(month))])
        for j, item in enumerate(date):
            date[j] = item.replace('[', '')
        for j, item in enumerate(date):    
            date[j] = item.replace(']','')
        date=date.astype(int)
        
        #unpack the third layer - science products
        #skip metadata - only contains readme
        sci = f.get('Column')
        print(sci.keys())
        #get the column data
        NO2_slant = np.array(sci.get('NO2_SlantColumn')).T
        NO2_below = np.array(sci.get('NO2_RetrievedVerticalColumnBelow')).T
        
        #correct & combine the date and time
        date = pd.to_datetime(date, format='%m%d%Y')
        timestamp = timestamp.flatten()
        times = pd.to_timedelta(timestamp,unit = 'h')
        my_datetime = pd.to_datetime(date + times)
        
    else: #if uppercase version - proceed
        #unpack the first layer - geolocation
        geoloc = f.get('GEOLOCATION_PARAMETERS')
        print(geoloc.keys())
        #get the parameters we need from this layer
        altitude = np.array(geoloc.get('ALT'))
        lat = np.array(geoloc.get('LAT'))
        lon = np.array(geoloc.get('LON'))
        timestamp = np.array(geoloc.get('TIME_STAMP'))
        date = geoloc['DATE'][:].astype(int) #convert from bytes to int
    
        #unpack the third layer - science products
        #skip metadata - only contains readme
        sci = f.get('SCIENCE_PRODUCTS')
        print(sci.keys())
        #get the column data
        NO2_slant = np.array(sci.get('NO2_SLCOL'))
        NO2_below = np.array(sci.get('VCDNO2BELOWAIRCRAFT'))
        
        #correct & combine the date and time
        date = date.flatten()
        date = pd.to_datetime(date, format='%m%d%Y')
        timestamp = timestamp.flatten()
        times = pd.to_timedelta(timestamp,unit = 'h')
        my_datetime = pd.to_datetime(date + times)
    
    #save all the data we extracted as a dataframe
    df = pd.DataFrame(index=my_datetime)
    df['datetime'] = my_datetime
    df['latitude'] = lat
    df['longitude'] = lon
    df['altitude'] = altitude
    
    #slant columns will load differently based on format
    
    #for lowercase, import into dataframe as is
    if f.get('GEOLOCATION_PARAMETERS') is None:
        df['NO2_slant'] = NO2_slant
        df['NO2_below'] = NO2_below
    #for uppercase, need to specify columns
    else:
        df['NO2_slant'] = NO2_slant[:,0]
        df['NO2_below'] = NO2_below[:,0]
        
    #close out of this file
    f.close()
     
    #retime to minutely averages
    df = df.resample('T').mean()
    
    #get rid of any empty or missing rows in dataframe
    df = df.dropna()

    #save out the final (raw) data
    savePath = os.path.join(path,'{}.csv'.format(fileList[i]))
    df.to_csv(savePath)
