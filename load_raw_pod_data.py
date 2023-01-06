# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 08:49:46 2023
@author: okorn

Code will automatically ignore the string at the top
Need to manually delete the rows of strings at the bottom of each txt file
"""

#Import in necessary packages
from tkinter.filedialog import askdirectory
import os
import pandas as pd

#Prompt user to select main folder for analysis
path = askdirectory(title='Select Folder for analysis').replace("/","\\")

#Give pod names to loop through
#podList = ['D0','D3','D4','D6','D8','F1','F3','F4','F5','F6','F7','F8','F9','N3','N4','N5','N7','N8']
podList = ['D6','D8','F6','N7','N8']

#loop through each pod
for k in range(len(podList)):
    #get another path for each individual pod folder
    path2 = os.path.join(path,podList[k])

    #Get the list of files from this directory
    from os import listdir
    from os.path import isfile, join
    fileList = [f for f in listdir(path2) if isfile(join(path2,f))]

    #create a dictionary to hold our data from each file
    data_dict = {}
  
    #iterate over each file in the pod folder
    for i in range(len(fileList)-1):
    
        #Create full file path for reading file
        filePath = os.path.join(path2, fileList[i])
    
        #load in the file
        temp = pd.read_csv(filePath,sep=',', header=0)
                
        #replace instances of "UPOD" with "YPOD" (for matlab readability)
        temp['Model'] = temp['Model'].replace('UPOD{}'.format(podList[k]),'YPOD{}'.format(podList[k]))
    
        #Save this into our data dictionary
        data_dict['{}'.format(fileList[i])] = temp
    
    #concatenate all of our data into 1 array
    full_data = pd.concat(data_dict.values())

    #save out the final data
    savePath = os.path.join(path2,'YPOD{}_field.txt'.format(podList[k]))
    full_data.to_csv(savePath)