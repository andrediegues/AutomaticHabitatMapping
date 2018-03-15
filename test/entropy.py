#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:40:08 2018

@author: diegues
"""

from skimage.io import imread
from skimage.measure import shannon_entropy
import os

def main():
    path = '/home/diegues/belinho/2017-04-10/logs/lauv-xtreme-2/20170411/101045_plan1/mra/filtered_sss_images/'
    imgspath = os.listdir(path) 
    for imgpath in [e for e in imgspath if 'png' in e]:
        img = imread(path + imgpath, True)
        print(imgpath,shannon_entropy(img))
    

if __name__ == '__main__':
    main()