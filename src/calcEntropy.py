#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:32:47 2018

@author: diegues
"""

from skimage.io import imread
from skimage.measure import shannon_entropy
import pandas as pd
import os
import sys

def main():
    os.chdir(sys.argv[1])
    data = pd.read_csv("positions.csv")
    folderpath = "icm/"
    entropy = []
    new_data = pd.DataFrame()
    new_data['filename'] = pd.unique(data['filename'])
    for imagename in pd.unique(data['filename']):
        print(os.path.abspath(imagename))
        e = shannon_entropy(imread(imagename + '.png'))
        if e < 0:
            e = 0
        entropy.append(e)
    new_data['entropy'] = entropy
    new_data.to_csv("entropy.csv", index=False)
    
if __name__ == '__main__':
    main()
