#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 13:52:52 2018

@author: diegues
"""

import pandas as pd
import os

path = "/home/diegues/andre.diegues@lsts.pt/ProcessedImages/01_05_18/"

labeled_data = pd.DataFrame(columns=['filename', 'timestamp', 'latitude', 'longitude', 'roll', 'pitch', 'entropy', 'date', 'depth', 
                                     'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'species', 'AphiaID'])

unlabeled_data = pd.DataFrame(columns=['filename', 'timestamp', 'latitude', 'longitude', 'roll', 'pitch', 'entropy', 'date', 'depth', 
                                     'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'species', 'AphiaID'])

total_data = pd.DataFrame(columns=['filename', 'timestamp', 'latitude', 'longitude', 'roll', 'pitch', 'entropy', 'date', 'depth', 
                                     'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'species', 'AphiaID'])

for folder in [f for f in os.listdir(path) if os.path.isdir(path+f)]:
    datafile = path + folder + "/" + folder + ".csv"
    if not os.path.exists(datafile):
        print(datafile , "doesn't exist!")
        continue
    print('reading',folder)
    data = pd.read_csv(datafile)
    total_depth = data['altitude'] + data['depth']
    data = data.drop(['altitude', 'depth'], axis = 1)
    data['depth'] = total_depth
    targetsfile = path + folder + "/" + folder + "-targets.csv"
    if not os.path.exists(targetsfile):
        print(targetsfile , "doesn't exist!")
        continue
    targets = pd.read_csv(targetsfile, names=['filename', 'date', 'longitude', 'latitude', 'depth', 'EunisCode', 'EunisName', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 
'species', 'AphiaID'])[1:]
    targets = targets.drop(['date', 'longitude', 'latitude', 'depth'], axis=1)
    join_dfs = pd.merge(data, targets, on='filename', how='outer')
    print(join_dfs.EunisCode[:3].isnull())
    non_empty_targets = join_dfs[join_dfs['EunisCode'].notnull()]
    print(non_empty_targets.head())
    empty_targets = join_dfs[join_dfs['EunisCode'].isnull()]
    labeled_data = labeled_data.append(non_empty_targets)
    unlabeled_data = unlabeled_data.append(empty_targets)
    total_data = total_data.append(join_dfs)
    
labeled_data.to_csv(path + "labeled_data.csv", index = False)
unlabeled_data.to_csv(path + "unlabeled_data.csv", index = False)
total_data.to_csv(path + "total_data.csv", index = False)
classes = labeled_data.level3.unique()
classesfile = open(path + "classes.txt", "w")
for c in classes:
    classesfile.write(c + "\n")
classesfile.close()

