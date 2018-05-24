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
data = pd.read_csv('mra/FilteredPhotos/positions.csv', names=['filename', 'timestamp', 'latitude', 'longitude', 'altitude', 'roll', 'pitch', 'depth', 'entropy'])[1:]
#print(data['entropy'].astype(float))
#print(data.entropy.astype(float) <= float(value))
namesToCopy = data[data['entropy'].astype(float) <= float(value)]
#print(namesToCopy)
os.mkdir(new_folder)
for file in namesToCopy['filename']:
    if os.path.isfile(folder + 'plt_wb_' + file):
        copyfile(folder + 'plt_wb_' + file, new_folder + '/' + file)
     
namesToCopy.to_csv(new_folder + '/' + logpath.split('/')[-1] + '.csv', index = False)
