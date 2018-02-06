#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:49:11 2017

@author: diegues
"""
# tried numba but increased the processing time by almost a double of what was taking without it
import cv2
import numpy
import itertools as it

def grayscale(imgname):
    return cv2.imread(imgname, 0)

def bluefilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,0]
    
def greenfilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,1]

def redfilter(imgname, img = None):
    if img is None:
        img = cv2.imread(imgname)
    return img[:,:,2]

def negativefilter(imgname):
    img = cv2.imread(imgname)
    return 255 - img

def drm(imgname):
    img = cv2.imread(imgname)
    return max(img.ravel()) - img

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

def linearStretch(img):
    if min(img.ravel()) == 0:
        bot = numpy.percentile(img.ravel(), 1)
    else:
        bot = min(img.ravel())
    if max(img.ravel()) == 255:
        top = numpy.percentile(img.ravel(), 99)
    else:
        top = max(img.ravel())
        
    hashmap = createHash(img, bot, top)
    img2 = img
    for i, j in it.product(range(img2.shape[0]), range(img2.shape[1])):
        img2[i,j] = hashmap[img2[i,j]]
    return img2

def createROI(img):
    return img[150:840, 220:1140]

def powerStretch(img): # not so good but worth a try
    img2 = img
    img2 = img2.astype(numpy.float)
    c = (img2.max()) / (img2.max()**(2))
    for i in range(0,img2.shape[0]-1):
        for j in range(0,img2.shape[1]-1):
            img2[i,j] = numpy.int(c*img2[i,j]**(2))

    img2 = img2.astype(numpy.uint8)
    return img2

def pseudocoloring(imgname):
    img = cv2.imread(imgname)
    return cv2.applyColorMap(img, cv2.COLORMAP_WINTER)

def rgbStretch(imgname):
    img = cv2.imread(imgname)
    stretched_blue = linearStretch(bluefilter(imgname, img))
    stretched_green = linearStretch(greenfilter(imgname, img))
    stretched_red = linearStretch(redfilter(imgname, img))
    m = cv2.merge((stretched_blue, stretched_green, stretched_red))
    return m

def findmax(img):
    maxpixel = [0,0,0]
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        if sum(img[i,j]) > sum(maxpixel):
            maxpixel = img[i,j]
            
    return maxpixel

def rescale(pixel, white):
    pixel[0] *= white[0]
    if pixel[0] > 255:
        pixel[0] = 255
    
    pixel[1] *= white[1]
    if pixel[1] > 255:
        pixel[1] = 255
    
    pixel[2] *= white[2]
    if pixel[2] > 255:
        pixel[2] = 255

    return pixel

def whitebalance(img):
    newwhite = findmax(img)
    scale = [255 / e for e in newwhite]
    newimg = img
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        newimg[i,j] = rescale(img[i,j],scale)
    return newimg

def integratedColorModel(imgname):
    rgbcs = rgbStretch(imgname)
    hlsimg = cv2.cvtColor(rgbcs, cv2.COLOR_RGB2HLS)    
    hue = hlsimg[:,:,0]
    light = hlsimg[:,:,1]
    saturation = hlsimg[:,:,2]
    lightcs = linearStretch(light)
    saturationcs = linearStretch(saturation)
    hlscs = cv2.merge((hue,lightcs,saturationcs))
    imc = cv2.cvtColor(hlscs, cv2.COLOR_HLS2RGB)
   
    return imc

