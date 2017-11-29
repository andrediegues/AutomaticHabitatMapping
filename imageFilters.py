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
            if img[i,j] <= bot:
                hashmap[img[i,j]] = 0
            elif img[i,j] > top:
                hashmap[img[i,j]] = 255
            else:
                hashmap[img[i,j]] = 255 * ((img[i,j] - bot) / (top - bot))
    return hashmap

def linearStretch(img):
    bot1percent = numpy.percentile(img.ravel(), 1)
    top99percent = numpy.percentile(img.ravel(), 99)
    hashmap = createHash(img, bot1percent, top99percent)
    img2 = img
    #img2 = map(hashmap, it.product(range(img2.shape[0]), range(img2.shape[1])))
    #cv2.imshow("img2", img2)
    #cv2.waitKey()
    for i, j in it.product(range(img2.shape[0]), range(img2.shape[1])):
        img2[i,j] = hashmap[img2[i,j]]
    return img2[150:840, 220:1140]

def powerStretch(img): # not so good but worth a try
    img2 = img
    img2 = img2.astype(numpy.float)
    c = (img2.max()) / (img2.max()**(0.5))
    for i in range(0,img2.shape[0]-1):
        for j in range(0,img2.shape[1]-1):
            img2[i,j] = numpy.int(c*img2[i,j]**(0.5))

    img2 = img2.astype(numpy.uint8)
    return img2

def pseudocoloring(imgname):
    img = cv2.imread(imgname)
    return cv2.applyColorMap(img, 5)