#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:35:30 2018

@author: diegues
"""

import sys 
import cv2
import os
from itertools import product 

def findmax(img):
    maxpixel = [0,0,0]
    for i,j in product(range(img.shape[0]), range(img.shape[1])):
        if sum(img[i,j]) > sum(maxpixel):
            maxpixel = img[i,j]
            
    return maxpixel

def rescale(pixel, white):
    pixel[2] *= white[2]
    if pixel[2] > 255:
        pixel[2] = 255
    
    pixel[1] *= white[1]
    if pixel[1] > 255:
        pixel[1] = 255
    
    pixel[0] *= white[0]
    if pixel[0] > 255:
        pixel[0] = 255
    
    return pixel

def whitebalance(img):
    newwhite = findmax(img)
    print(newwhite)
    scale = [255 / e for e in newwhite]
    print(scale)
    newimg = img
    for i,j in product(range(img.shape[0]), range(img.shape[1])):
        newimg[i,j] = rescale(img[i,j],scale)
    return newimg

def main():
    path = sys.argv[1]
    photolist = os.listdir(path)
    if not os.path.exists(path + '/../wb'):
        os.mkdir(path + '/../wb')
    for img in photolist:
        image = cv2.imread(path + img)
        newimg = whitebalance(image)
        cv2.imwrite(path + '/../wb/' + img, newimg)
    



if __name__ == '__main__':
    main()