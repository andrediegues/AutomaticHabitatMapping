#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:02:43 2017

@author: diegues

This is the main module. It contains some of the possible actions in order to process/transform an image (see options below). 
If no option is provided, it applies the RGB constrast stretching of the images.

OPTIONS:
    -l (--linearstretch): Applies the linear stretching to the image. 
    -n (--nonlinearstretch): Returns the contrast stretch using a nonlinear function.
    -p (--pseudocolor): Applies the pseudocolor colormap of the images in the LinearStretching folder, If the folder doesn't exist this folder is generated.
    
"""
from functools import partial
import os
import sys
import cv2
import imageFilters as imf
import multiprocessing as mp
import time

def applyLinearStretching(photos_path):
    list_of_photos = os.listdir(os.getcwd())
    linear_path = '../LinearStretching/'
    createDir(linear_path)
    
    pool = mp.Pool(processes=mp.cpu_count())
    func = partial(linearStretchHandler, linear_path)
    
    time0 = time.time()
    pool.map(func, list_of_photos)
    time1 = time.time()
    
    print("Linear stretching took",int((time1 - time0) // 60), "minutes and", round((time1 - time0) % 60), "seconds.")


def applyPowerStretching(photos_path):
    list_of_photos = os.listdir(os.getcwd())
    nonlinear_path = '../NonLinearStretching/'
    createDir(nonlinear_path)
    
    pool = mp.Pool(processes=mp.cpu_count())
    func = partial(nonLinearStretchHandler, nonlinear_path)
    
    time0 = time.time()
    pool.map(func, list_of_photos)
    time1 = time.time()
    
    print("Non-linear stretching took",int((time1 - time0) // 60), "minutes and", round((time1 - time0) % 60), "seconds.")

def applyPseudoColor(photos_path):
    contrast_path = '../LinearStretching/'
    if not checkPath(contrast_path):
        io = input("Would you like to run the linear stretching so that this option can be executed? [Y/n]")
        if 'n' in io:
            sys.exit(1)
        applyLinearStretching(photos_path)
    
    list_of_cs_photos = os.listdir(contrast_path)
    pseudocolor_path = "../PseudoColor/"
    createDir(pseudocolor_path)
    
    colormap = partial(pseudoColorHandler, contrast_path, pseudocolor_path)
    pool = mp.Pool(processes=mp.cpu_count())
    
    time0 = time.time()
    pool.map(colormap, list_of_cs_photos)
    time1 = time.time()
    
    print("Pseudocoloring took",int((time1 - time0) // 60), "minutes and", round((time1 - time0)% 60), "seconds.")

def applyMergeStretch(photos_path):
    list_of_photos = os.listdir(os.getcwd())
    rgbstretch_path = "../RGBstretch/"
    createDir(rgbstretch_path)
    
    pool = mp.Pool(processes = mp.cpu_count())
    rgb = partial(rgbStretchHandler, rgbstretch_path)
    
    time0 = time.time()
    pool.map(rgb, list_of_photos)
    time1 = time.time()
    
    print("RGB stretching took",int((time1 - time0) // 60), "minutes and", round((time1 - time0)% 60), "seconds.")
        
def checkPath(path):
    if not os.path.exists(path):
        print("ERROR: The path", path, "doesn't exist!")
        return False
    return True

def createDir(path): 
    if not os.path.exists(path):
        os.mkdir(path)
        
def nonLinearStretchHandler(contrast_path, photoname):
    gray_photo = imf.grayscale(photoname)
    pow_stretch_name = 'nl_' + photoname
    if pow_stretch_name not in os.listdir(contrast_path):
        pow_stretch_gray = imf.powerStretch(gray_photo)
        cv2.imwrite(contrast_path + pow_stretch_name, pow_stretch_gray)


def rgbStretchHandler(rgb_path, photoname):
    rgbname = "rgb_" + photoname
    if rgbname not in os.listdir(rgb_path):
        rgb_photo = imf.rgbStretch(photoname)
        cv2.imwrite(rgb_path + rgbname, rgb_photo)

def linearStretchHandler(contrast_path, photoname):
    gray_photo = imf.grayscale(photoname)
    lin_stretch_name = 'l_' + photoname
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
        if not checkPath(photos_path):
            sys.exit(1) 
        os.chdir(photos_path)
        applyMergeStretch(photos_path)
        
        
    elif len(sys.argv) == 3:
        photos_path = sys.argv[2]
        if not checkPath(photos_path):
            sys.exit(1)
        os.chdir(photos_path)
        if "--pseudocolor" in sys.argv or "-p" in sys.argv:
            applyPseudoColor(photos_path)
        elif "--linearstretch" in sys.argv or "-l" in sys.argv:
            applyLinearStretching(photos_path)
        elif "--nonlinearstretch" in sys.argv or "-n" in sys.argv:
            applyPowerStretching(photos_path)
        

if __name__ == '__main__':
    main()
    
