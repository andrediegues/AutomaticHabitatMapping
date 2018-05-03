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
    data = pd.read_csv("positions.csv", names=['filename', 'timestamp', 'longitude', 'latitude'])[1:]
    folderpath = "Original/"
    entropy = []
    for imagename in data['filename']:
        e = shannon_entropy(imread(folderpath + imagename + '.jpg'))
        if e < 0:
            e = 0
        entropy.append(e)
    data['entropy'] = entropy
    data.to_csv("positions.csv")
    
if __name__ == '__main__':
    main()