# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:06:32 2024

@author: okorn
"""

# import libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

#list of pollutants to loop through
pollutants = ['SO2','NO2']

for n in range(len(pollutants)):

    #Prompt user to select folder for analysis
    #path = 'C:\\Users\\okorn\\Documents\\2023 Deployment\\Modeling Surface Concentrations\\EPA\\Raw Data\\{}'.format(pollutants[n])
    path = 'C:\\Users\\kokorn\\Documents\\Modeling Surface Concentrations\\EPA\\Raw Data\\{}'.format(pollutants[n])

    #get one large dataframe to save all our data into
    EPA = pd.DataFrame()

    #Get the list of files from this directory
    from os import listdir
    from os.path import isfile, join
    fileList = [f for f in listdir(path) if isfile(join(path, f))]
    #loop through each file
    for i in range(len(fileList)):

        #Create full file path for reading file
        filePath = os.path.join(path, fileList[i])
 
        #load in the file
        temp = pd.read_csv(filePath,usecols=['Site Num','Latitude', 'Longitude','Date GMT', 'Time GMT','Sample Measurement'])
    
        #remove the rows we don't need based on each pollutant
        if pollutants[n] == 'O3':
            values_to_keep = [5,9002,27,9003,43,3003,2006,2003,18,6,11,133,44,124,12,48,8,1010]
        elif pollutants[n] == 'NO2':
            values_to_keep = [27,9003,43,2006,18,6,11,122,44,124,48,8,1010,3006,8,15,24]
        elif pollutants[n] == 'SO2':
            values_to_keep = [5,27,43,18,6,133,124,48,8,1010,3006,8,15]

        # Filter the DataFrame
        temp = temp[temp['Site Num'].isin(values_to_keep)]
    
        #combine the date & time columns
        temp['datetime'] = pd.to_datetime(temp['Date GMT'] + ' ' + temp['Time GMT'])
    
        #clean up the dataframe
        del temp['Date GMT']
        del temp['Time GMT']
    
        #make the datetime the index
        temp = temp.set_index('datetime')
    
        #append to the overall dataframe
        EPA = EPA.append(temp)

    #Sort the DataFrame by location in ascending order
    EPA = EPA.sort_values(by='Site Num', ascending=True)
    
    #Change the repeat location identifier to something different
    EPA.loc[(EPA['Site Num'] == 8) & (EPA['Latitude'] == 37.103733), 'Site Num'] = 88

    #Map each site number to the site name
    map = {5: 'Cornwall',
       9002: 'MadisonCT',
       27: 'NewHaven',
       9003: 'Westport',
       43: 'WashingtonDC',
       3003: 'Bluehill',
       2006: 'Lynn',
       2003: 'CapeElizabeth',
       18: 'Londonderry',
       6: 'Bayonne',
       11: 'NewBrunswick',
       133: 'Bronx',
       44: 'Oldfield',
       124: 'Queens',
       12: 'Bristol',
       48: 'Philadelphia',
       8: 'Pittsburgh',
       1010: 'EastProvidence',
       3006: 'Hawthorne',
       15: 'Detroit',
       24: 'AldineTX',
       88: 'Hampton'
       }

    #Group the DataFrame by the specified column
    grouped = EPA.groupby('Site Num')

    #Create a dictionary to hold the split DataFrames with the corresponding names as keys
    dataframes = {}

    #Use the mapping to get the corresponding string name
    for key, group in grouped:
        df_name = map[key]
        dataframes[df_name] = group

    #Clean up the format before saving it out
    for name, dataframe in dataframes.items():
        dataframe = dataframe.drop(columns=['Latitude','Longitude','Site Num'])
        dataframe = dataframe.rename(columns={'Sample Measurement': 'O3'})
   
        #Save each DataFrame to a CSV
        #spath = 'C:\\Users\\okorn\\Documents\\2023 Deployment\\Modeling Surface Concentrations\\EPA\\Output Data'
        spath = 'C:\\Users\\kokorn\\Documents\\Modeling Surface Concentrations\\EPA\\Output Data'

        save_path = os.path.join(spath, f"EPA_{name}_{pollutants[n]}.csv")
        dataframe.to_csv(save_path, index=True)  # Adjust parameters as needed for your use case
        print(f"DataFrame '{name}' saved to '{save_path}'")
