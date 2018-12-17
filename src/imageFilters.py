#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:49:11 2017

@author: diegues

This module contains functions with image transformations. It serves as an auxiliary module to 'ImageProcessing.py'.
"""


import cv2
import numpy as np
import itertools as it

# Returns a grayscale image of the path 'imgname'
def grayscale(imgname):
    return cv2.imread(imgname, 0)

# Returns the blue values of the image of the path 'imgname'. Optionally you can provide the image as an argument.
def bluefilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,0]
    
# Returns the green values of the image of the path 'imgname'. Optionally you can provide the image as an argument.
def greenfilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,1]

# Returns the red values of the image of the path 'imgname'. Optionally you can provide the image as an argument.
def redfilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,2]

# Returns the negative image of the path 'imgname'.
def negativefilter(imgname):
    img = cv2.imread(imgname)
    return 255 - img

# Returns the Dynamic Range Manipulation of the image of the path 'imgname'. 
def drm(imgname):
    img = cv2.imread(imgname)
    return max(img.ravel()) - img

# Returns an hash of values that compute Contrast Stretching formula to prevent recalculating the same values over and over
def createHash(img, bot, top):
    hashmap = {}
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        if img[i,j] not in hashmap:
            if img[i,j] <= bot:
                hashmap[img[i,j]] = 0
            elif img[i,j] > top:
                hashmap[img[i,j]] = 255
            else:
                hashmap[img[i,j]] = 255 * ((img[i,j] - bot) / (top - bot))
    return hashmap

# Contrast Stretching processing
def linearStretch(img):
    bot = min(img.ravel())
    top = max(img.ravel())
        
    hashmap = createHash(img, bot, top)
    img2 = img
    for i, j in it.product(range(img2.shape[0]), range(img2.shape[1])):
        img2[i,j] = hashmap[img2[i,j]]
    return img2

# Power-level Transformation
def powerStretch(img):
    img2 = img
    img2 = img2.astype(np.float)
    c = (img2.max()) / (img2.max()**(2))
    for i in range(0,img2.shape[0]-1):
        for j in range(0,img2.shape[1]-1):
            img2[i,j] = np.int(c*img2[i,j]**(2))

    img2 = img2.astype(np.uint8)
    return img2

# Applies colormap to grayscale image
def pseudocoloring(imgname):
    img = cv2.imread(imgname)
    return cv2.applyColorMap(img, cv2.COLORMAP_WINTER)

# Applies Contrast Stretching to each channel of an RGB image, merging them afterwards (not optimal result, see HSVConstrastStretch function that uses HSV color model)
def rgbStretch(imgname):
    img = cv2.imread(imgname)
    stretched_blue = linearStretch(bluefilter(imgname, img))
    stretched_green = linearStretch(greenfilter(imgname, img))
    stretched_red = linearStretch(redfilter(imgname, img))
    m = cv2.merge((stretched_blue, stretched_green, stretched_red))
    return m

# Secundary function to find each RGB channel's maximum intensity in the image for the Max-White algorithm.
def findmax(img):
    maxpixel = img[0,0]
    maxBlue = maxpixel[0]
    maxGreen = maxpixel[1]
    maxRed = maxpixel[2]
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        bluePixel = img[i,j,0]
        greenPixel = img[i,j,1]
        redPixel = img[i,j,2]
        if bluePixel > maxBlue:
            maxBlue = img[i,j,0]
        if greenPixel > maxGreen:
            maxGreen = img[i,j,1]
        if redPixel > maxRed:
            maxRed = img[i,j,2]
            
    return [maxBlue,maxGreen,maxRed]

# Function to compute each pixel's gain for the Max-White algorithm.
def rescale(pixel, white):
    val = pixel * white
    if pixel * white > 255:
        return 255 
    return val

# Max-White algorithm that returns a brighter image with correction of colors.
def whitebalance(imgname):
    img = cv2.imread(imgname)
    newwhite = findmax(img)
    scale = [255 / e for e in newwhite]
    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]
    hb = {}
    hg = {}
    hr = {}
    for e in list(set(b.ravel())):
        hb[e] = rescale(e, scale[0])
    for e in list(set(g.ravel())):
        hg[e] = rescale(e, scale[1])
    for e in list(set(r.ravel())):
        hr[e] = rescale(e, scale[2])
    newimg = img
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        newimg[i,j] = np.array([hb[img[i,j][0]],hg[img[i,j][1]],hr[img[i,j][2]]])
    return newimg

# HSV color model stretching of saturation and value channels to perform Contrast Stretching to a RGB image.
def integratedColorModel(imgname):
    img = cv2.imread(imgname)
    hsvimg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)    
    hue = hsvimg[:,:,0]
    saturation = hsvimg[:,:,1]
    value = hsvimg[:,:,2]
    valuecs = linearStretch(value)
    saturationcs = linearStretch(saturation)
    hlscs = cv2.merge((hue,saturationcs,valuecs))
    im = cv2.cvtColor(hlscs, cv2.COLOR_HSV2RGB)
   
    return im

