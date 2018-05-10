#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:53:19 2018

@author: diegues
"""

from skimage.measure import shannon_entropy
from skimage.io import imread
import os
import numpy as np

path = "/home/diegues/Reuniões OMARE/16-04-18/varrimento_frames/"
files = os.listdir(path)
entropies = []
for file in files:
    img = imread(path + file, True)
    entropies.append(shannon_entropy(img))
entropies = np.asarray(entropies)
np.median(entropies)
np.mean(entropies)
np.min(entropies)
np.max(entropies)