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

folder = 'mra/FilteredPhotos/Original/'
logpath = os.path.abspath(sys.argv[1])
os.chdir(logpath)
new_folder = logpath + '/' + logpath.split('/')[-1]
new_names = []
date = logpath.split('/')[-2][-2:] + '/' + logpath.split('/')[-2][-4:-2] + '/' + logpath.split('/')[-2][-6:-4]
dates = []
data = pd.read_csv(logpath + '/mra/FilteredPhotos/positions.csv')
#value = data.describe()['entropy']['75%']
#answer = input('75%: ' + str(value) + '\nIntroduce a different value (enter ''no'' to maintain the same):')
#if('n' not in answer):
#    value = answer
#namesToCopy = data[data['entropy'].astype(float) <= float(value)]
namesToCopy = data
os.mkdir(new_folder)
for file in namesToCopy['filename']:
    if os.path.isfile(folder + file + '.jpg'):
        copyfile(folder + file+ '.jpg', new_folder + '/' + new_folder.split('/')[-1] + '_' + file+ '.jpg')
        new_names.append(new_folder.split('/')[-1] + '_' + file+ '.jpg')
        dates.append(date)
namesToCopy.loc[:,('date')] = list(dates)
namesToCopy.loc[:, ('filename')] = list(new_names)
namesToCopy.to_csv(new_folder + '/' + logpath.split('/')[-1] + '.csv', index = False)
