#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 13:52:52 2018

@author: diegues
"""

import pandas as pd
import os

path = "/home/diegues/Desktop/ProcessedImages/"

labeled_data = pd.DataFrame(columns=['filename', 'timestamp', 'latitude', 'longitude', 'roll', 'pitch', 'entropy', 'date', 'depth', 
                                     'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'species', 'AphiaID'])

for folder in [f for f in os.listdir(path) if os.path.isdir(path+f)]:
    datafile = path + folder + "/" + folder + ".csv"
    if not os.path.exists(datafile):
        print(datafile + "doesn't exist!")
        break
    data = pd.read_csv(datafile, 
                       names=['filename', 'timestamp', 'latitude', 'longitude', 'altitude', 'roll', 'pitch', 'depth', 'entropy', 'date'])[1:]
    data = data.drop(['altitude', 'depth'], axis = 1)
    targetsfile = path + folder + "/" + folder + "-targets.csv"
    if not os.path.exists(targetsfile):
        print(targetsfile + "doesn't exist!")
        continue
    targets = pd.read_csv(targetsfile,
                          names=['filename', 'date', 'longitude', 'latitude', 'depth', 'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 
                                 'species', 'AphiaID'])[1:]
    targets = targets.drop(['date', 'longitude', 'latitude'], axis=1)
    join_dfs = pd.merge(data, targets, on='filename', how='outer')
    non_empty_targets = join_dfs[join_dfs['EunisCode'].notnull()]
    labeled_data = labeled_data.append(non_empty_targets)
    
labeled_data.to_csv(path + "labeled_data.csv", index = False)
classes = labeled_data.EunisCode.unique()
classesfile = open(path + "classes.txt", "w")
for c in classes:
    classesfile.write(c + "\n")
classesfile.close()

