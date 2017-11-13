#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:02:43 2017

@author: diegues
"""

import os
import sys
import cv2


def main():
    if len(sys.argv) < 2:
        print("ERROR: Please provide the path to the folder of the photos\n\tpython3 ImageProcessing.py /the/path/to/the/photos")
        sys.exit(1)    
    photos_path = sys.argv[1]
    if not os.path.exists(photos_path):
        print("ERROR: The path provided doesn't exist!")
        sys.exit(1)
    list_of_photos = os.listdir(photos_path)
    if False in [True for photo in list_of_photos if "jpg" in photo]:
        print("ERROR: Not all the files are images!")
        sys.exit(1)
    os.chdir(photos_path)
    gray_path = '../GrayScale/'
    if not os.path.exists(gray_path):
        os.mkdir(gray_path)
    
    for photoname in list_of_photos:
        gray_photo = cv2.imread(photoname, 0)
        cv2.imwrite(gray_path + 'gray_' + photoname, gray_photo)

if __name__ == '__main__':
    main()
    
