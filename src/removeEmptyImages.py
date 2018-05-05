#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:12:24 2018

@author: diegues
"""

import sys
import pandas as pd
import os

folder = 'Original/'
os.chdir(sys.argv[1])
value = float(sys.argv[2])
data = pd.read_csv('positions.csv', names=['filename', 'timestamp', 'longitude', 'latitude', 'altitude', 'roll', 'pitch', 'depth', 'entropy'])[1:]
namesToRemove = data[data['entropy'].astype(float) < value]

for file in namesToRemove['filename']:
    if os.path.isfile(folder + file):
        os.remove(folder + file)
     
newData = data[data['entropy'].astype(float) >= value]
newData.to_csv('positions.csv')