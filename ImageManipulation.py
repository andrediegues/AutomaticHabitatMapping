#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:03:12 2017

@author: diegues
"""
import sys
import os
import cv2
import imageFilters


def main():
    if len(sys.argv) < 2:
        print("ERROR: not enough arguments")
        sys.exit(1)
    imgpath = sys.argv[1]
    if not os.path.exists(os.path.abspath(imgpath)):
        print("ERROR: image doesn't exist")
        sys.exit(1)
    img = cv2.imread(imgpath, 0)
    img  = imageFilters.linearStretch(img)

if __name__ == "__main__":
    main()