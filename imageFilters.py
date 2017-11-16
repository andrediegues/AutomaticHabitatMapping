#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:49:11 2017

@author: diegues
"""

import cv2
import numpy
import itertools as it

def grayscale(imgname):
    return cv2.imread(imgname, 0)

def bluefilter(imgname):
    img = cv2.imread(imgname)
    return img[:,:,0]
    
def greenfilter(imgname):
    img = cv2.imread(imgname)
    return img[:,:,1]

def redfilter(imgname):
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
            if img[i,j] <= bot or img[i,j] > top:
                pass
            else:
                hashmap[img[i,j]] = 255 * ((img[i,j] - bot) / (top - bot))
    return hashmap

def linearStretch(img):
    new_min = 0
    new_max = 255
    bot1percent = numpy.percentile(img.ravel(), 1)
    top99percent = numpy.percentile(img.ravel(), 99)
    hashmap = createHash(img, bot1percent, top99percent)
    img2 = img
    for i, j in it.product(range(img2.shape[0]), range(img2.shape[1])):
        if img2[i,j] <= bot1percent:
            img2[i,j] = new_min
        elif img2[i,j] > top99percent:
            img2[i,j] = new_max
        else:
            img2[i,j] = hashmap[img2[i,j]]
    return img2

def powerStretch(img): # not so good but worth a try
    img2 = img
    img2 = img2.astype(numpy.float)
    c = (img2.max()) / (img2.max()**(0.5))
    for i in range(0,img2.shape[0]-1):
        for j in range(0,img2.shape[1]-1):
            img2[i,j] = numpy.int(c*img2[i,j]**(0.5))

    img2 = img2.astype(numpy.uint8)
    return img2