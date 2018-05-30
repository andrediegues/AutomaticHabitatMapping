#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:12:24 2018

@author: diegues
"""

import sys
import pandas as pd
import os
from shutil import copyfile

folder = 'mra/FilteredPhotos/PowerLawTransformStretching/'
logpath = os.path.abspath(sys.argv[1])
os.chdir(logpath)
new_folder = logpath + '/' + logpath.split('/')[-1]
value = sys.argv[2]
new_names = []
date = logpath.split('/')[-2][-2:] + '/' + logpath.split('/')[-2][-4:-2] + '/' + logpath.split('/')[-2][-6:-4]
dates = []
data = pd.read_csv('mra/FilteredPhotos/positions.csv', names=['filename', 'timestamp', 'latitude', 'longitude', 'altitude', 'roll', 'pitch', 'depth', 'entropy'])[1:]
namesToCopy = data[data['entropy'].astype(float) <= float(value)]
os.mkdir(new_folder)
for file in namesToCopy['filename']:
    if os.path.isfile(folder + 'plt_wb_' + file):
        copyfile(folder + 'plt_wb_' + file, new_folder + '/' + new_folder.split('/')[-1] + '_' + file)
        new_names.append(new_folder.split('/')[-1] + '_' + file)
        dates.append(date)
namesToCopy.loc[:,('date')] = list(dates)
namesToCopy.loc[:, ('filename')] = list(new_names)
namesToCopy.to_csv(new_folder + '/' + logpath.split('/')[-1] + '.csv', index = False)
