# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:19:26 2023

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

#create a dictionary to hold our data from each file
data_dict = {}

#loop through each of the files & extract only the columns we need:
  #datetime, CO (dry)
  
#iterate over each file in the main folder
for i in range(len(fileList)-1):
    
    #Create full file path for reading file
    filePath = os.path.join(path, fileList[i])
    
    #load in the file
    temp = h5py.File(filePath, 'r')
    
    with h5py.File(filePath, "r") as f:
        # Print all root level object names (aka keys) 
        # these can be group or dataset names 
        print("Keys: %s" % f.keys())
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]

        # get the object type for a_group_key: usually group or dataset
        print(type(f[a_group_key])) 

        # If a_group_key is a group name, 
        # this gets the object names in the group and returns as a list
        data = list(f[a_group_key])

        # If a_group_key is a dataset name, 
        # this gets the dataset values and returns as a list
        data = list(f[a_group_key])
        # preferred methods to get dataset values:
        ds_obj = f[a_group_key]      # returns as a h5py dataset object
        ds_arr = f[a_group_key][()]  # returns as a numpy array
 
    #Save this into our data dictionary
    data_dict['{}'.format(fileList[i])] = temp
    
#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#get the final data in a convenient format
full_data = full_data.rename(columns={'Time':'datetime','[CO_dry]_ppm': 'CO'})
CO = pd.DataFrame(full_data.index,full_data['CO'])

#save out the final data
savePath = os.path.join(path,'CO.csv')
CO.to_csv(savePath)