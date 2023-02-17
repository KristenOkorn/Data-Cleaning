# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:54:58 2023

Load in & reformat FRAPPE pressure data for BAO

@author: okorn
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd
from datetime import datetime, timedelta

#Prompt user to select folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Get the list of files from this directory
from os import listdir
from os.path import isfile, join
fileList = [f for f in listdir(path) if isfile(join(path, f))]

#create a datframe to hold our data from each file
data = pd.DataFrame()

#loop through each of the files & extract only the columns we need:
  #datetime, CO (dry)
  
#iterate over each file in the main folder
for i in range(len(fileList)-1):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #get info we need from the header
    with open(filePath, 'r') as f:
        lines = f.readlines()
        date = lines[6] #get the original datestamp to add to the time
        date = ",".join(date.split(",")[:3]) #only keep the first date
        date = date.replace(" ", "") #remove random whitespaces
        nullrows = lines[0] #get the number of lines to skip
        nullrows = ",".join(nullrows.split(",")[:1]) #only keep the first number
        nullrows = int(nullrows) - 1 #account for different indexing
    
    #load in the file
    temp = pd.read_csv(filePath,skiprows=nullrows,sep=',',encoding = "ISO-8859-1",
                       usecols = ['Start_UTC',' PRESS'])
    
    #remove empty spaces in data for workability
    temp.columns = temp.columns.str.strip() 
    
    #rename the HCHO column
    temp = temp.rename(columns={'PRESS': 'Pressure'})
    
    #correct the format of the datetimes
    #fix the HMS times
    temp['Start_UTC'] = [timedelta(seconds=t) for t in temp['Start_UTC']]
        
    #now reforrmat as a datetime
    date = datetime.strptime(date, "%Y,%m,%d")
    
    #add this to our times of day
    temp['datetime'] = temp['Start_UTC'] + date
    
    #get rid of what we don't need
    temp = temp.drop(columns=['Start_UTC'])
    
    #retime to minutely
    temp = temp.resample('T').mean()
        
    #drop any NaNs generated by the resampling
    temp = temp.dropna()
    
    #make the datetimes the index
    temp = temp.set_index('datetime')
   
    #Save this into our data dictionary
    data = data.append(temp)
    
#save out the final data
savePath = os.path.join(path,'NREL_Pressure.csv')
data.to_csv(savePath)