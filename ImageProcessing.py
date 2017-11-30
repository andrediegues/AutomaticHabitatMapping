#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:02:43 2017

@author: diegues

This is the module that isto called when filtering an image. It contains some of the possible filters to apply to an image. 

OPTIONS:
    --red: Returns the gray gradient of the red color.
    --blue: Returns the gray gradient of the blue color.
    --green: returns the gray gradient of the green color.
    --negative: Returns the negative color.
    --drm: Returns the gray gradient of the Dynamic Range Manipulation.
    --powerstretch: Returns the contrast stretch using a power function. In this case the power ** (1/2)
    --linearstretch: Returns the contrast stretch using a linear function.

"""
from functools import partial
import os
import sys
import cv2
import imageFilters as imf
import multiprocessing as mp
import time

def applyLinearStretching(photos_path):
    checkPath(photos_path)
    list_of_photos = os.listdir(photos_path)
    os.chdir(photos_path)
    gray_path = '../GrayScale/'
    contrast_path = '../ContrastStretching/'
    createDir(gray_path)
    createDir(contrast_path)
    
    pool = mp.Pool(processes=mp.cpu_count())
    func = partial(linearStretchHandler, gray_path, contrast_path)
    
    time0 = time.time()
    pool.map(func, list_of_photos)
    time1 = time.time()
    
    print("Linear stretching took",(time1 - time0) // 60, "minutes and", (time1 - time0)% 60, "seconds.")
    
def applyPseudoColor(photos_path):
    checkPath(photos_path)
    os.chdir(photos_path)
    contrast_path = '../ContrastStretching/'
    checkPath(contrast_path)
    list_of_cs_photos = os.listdir(contrast_path)
    pseudocolor_path = "../PseudoColor/"
    createDir(pseudocolor_path)
    
    colormap = partial(pseudoColorHandler, contrast_path, pseudocolor_path)
    pool = mp.Pool(processes=mp.cpu_count())
    
    time0 = time.time()
    pool.map(colormap, list_of_cs_photos)
    time1 = time.time()
    
    print("Pseudocoloring took",(time1 - time0) // 60, "minutes and", (time1 - time0)% 60, "seconds.")
        
def checkPath(path):
    if not os.path.exists(path):
        print("ERROR: The path",path,"doesn't exist!")
        sys.exit(1)

def createDir(path): 
    if not os.path.exists(path):
        os.mkdir(path)
        
def mergeGrayGradients(blue, green, red):
    stretched_blue = imf.linearStretch(blue)
    stretched_green = imf.linearStretch(green)
    stretched_red = imf.linearStretch(red)
    m = cv2.merge((stretched_blue, stretched_green, stretched_red))
    return cv2.fastNlMeansDenoisingColored(m, None, 4, 4, 7, 21)

def linearStretchHandler(gray_path, contrast_path, photoname):
    grayname = 'gray_' + photoname
    gray_photo = imf.grayscale(photoname)
    if grayname not in os.listdir(gray_path):
        cv2.imwrite(gray_path + grayname, gray_photo)
    #blue_photo = imf.bluefilter(photoname)
    #green_photo = imf.greenfilter(photoname)
    #red_photo = imf.redfilter(photoname)
    #mix_color_lin_stretch = mergeGrayGradients(blue_photo, green_photo, red_photo)
    #cv2.imwrite(color_path + 'cs_' + photoname, mix_color_lin_stretch)  
    lin_stretch_name = 'cs_' + photoname
    if lin_stretch_name not in os.listdir(contrast_path):
        lin_stretch_gray = imf.linearStretch(gray_photo)
        cv2.imwrite(contrast_path + lin_stretch_name, lin_stretch_gray) 
        
def pseudoColorHandler(contrast_path, pseudocolor_path, photoname):
    pseudocolor_name = "pseudo_" + photoname
    os.chdir(contrast_path)
    if pseudocolor_name not in os.listdir(pseudocolor_path):
        pseudocolor_photo = imf.pseudocoloring(photoname)
        cv2.imwrite(pseudocolor_path + pseudocolor_name, pseudocolor_photo)
        

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("ERROR: Please provide the path to the folder of the photos\n\t'python3 ImageProcessing.py /the/path/to/the/photos'\nor\n'python3 ImageProcessing.py --pseudocolor /the/path/to/the/photos'")
        sys.exit(1)
    elif len(sys.argv) == 2:
        photos_path = sys.argv[1]
        applyLinearStretching(photos_path)
        
    elif len(sys.argv) == 3 and "--pseudocolor" in sys.argv:
        photos_path = sys.argv[2]
        applyPseudoColor(photos_path)
        

if __name__ == '__main__':
    main()
    
