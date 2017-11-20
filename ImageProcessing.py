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


def mergeGrayGradients(blue, green, red):
    stretched_blue = imf.linearStretch(blue)
    stretched_green = imf.linearStretch(green)
    stretched_red = imf.linearStretch(red)
    return cv2.merge((stretched_blue, stretched_green, stretched_red))

def imageHandler(gray_path, contrast_path, photoname):
    grayname = 'gray_' + photoname
    if grayname not in os.listdir(gray_path):
        gray_photo = imf.grayscale(photoname)
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
    contrast_path = '../ContrastStretching/'
    #color_path = '../ContrastStretching/ColorMerge/'
    #gray_cs_path = '../ContrastStretching/GrayContrastStretch/'
    if not os.path.exists(gray_path):
        os.mkdir(gray_path)
    if not os.path.exists(contrast_path):
        os.mkdir(contrast_path)
    #if not os.path.exists(color_path):
     #   os.mkdir(color_path)
    #if not os.path.exists(gray_cs_path):
     #   os.mkdir(gray_cs_path)
    
    pool = mp.Pool(processes=mp.cpu_count())
    func = partial(imageHandler, gray_path, contrast_path)
    pool.map(func, list_of_photos)

if __name__ == '__main__':
    main()
    
