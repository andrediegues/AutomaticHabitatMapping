#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 14:57:43 2018

@author: diegues

Module that copy the data with less noise to a different folder. Change the folder path to your own.
"""

import pandas as pd
import os
from shutil import copyfile

folder = '/media/newdrive/20180501/ProcessedImages/'
df = pd.read_csv(folder + 'labeled_data.csv')
subfolders = [d for d in os.listdir(folder) if os.path.isdir(folder + d)]
filenames = df['filename']
new_folder = folder + 'LabeledData/'
if(not os.path.exists(new_folder)):
    os.mkdir(new_folder)

for f in filenames:
    for d in subfolders:
        if(d in f):
            copyfile(folder + d + '/' + f, new_folder + f)
            break
