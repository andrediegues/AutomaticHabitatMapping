#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:13:59 2018

@author: diegues
"""

import sys
import cv2
import imageFilters as imf
import itertools as it
import math
import numpy as np
from scipy.stats import rayleigh
from matplotlib import pyplot as plt

def splitHist(hist):
    rmin = hist.argmin()
    rmax = hist.argmax()
    rmid = math.floor((rmax - rmin) / 2 + rmin)
    #print(rmin, rmax, rmid, len(hist))
    l = hist[:rmid]
    r = hist[rmid:]
    #print(l)
    #print(r)
    return l, r

def rayleighStretch(hist):
    h = {}
    bot = hist.argmin()
    if bot == 0:
        bot = np.percentile(hist, 1)
    top = hist.argmax()
    if top == 255:
        top = np.percentile(hist, 99)
    newhist = hist
    #print(bot, top)    
    for pixel in newhist:
        #print(pixel[0])
        if pixel[0] < bot:
            pixel[0] = 0
        elif pixel[0] > top:
            pixel[0] = 255
        else:
            pixel[0] = (255 * ((pixel[0] - bot) / (top - bot)))
#        print(pixel)
    #print(newhist)
    val = rayleigh.pdf(newhist, scale=256)
    print(val)
    return h

def average(img, l, r):
    newimg = img
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        newimg[i,j] = (r[i,j] - l[i,j]) / 2 + l[i,j]
    return newimg

def main():
    imgname = sys.argv[1]
    img = cv2.imread(imgname)    
    b = imf.bluefilter(imgname)
    g = imf.greenfilter(imgname)
    r = imf.redfilter(imgname)
    
    bhist = cv2.calcHist([b], [0], None, [256], [0,256])
    ghist = cv2.calcHist([g], [0], None, [256], [0,256])
    rhist = cv2.calcHist([r], [0], None, [256], [0,256])
    #print(bhist.argmin())
    bl, br = splitHist(bhist)
    gl, gr = splitHist(ghist)
    rl, rr = splitHist(rhist)
    
    blrs = rayleighStretch(bl)
    #brrs = rayleighStretch(br)
    plt.subplot(121)
    plt.plot(bl)
    plt.subplot(122)
    plt.plot(br)
    #plt.subplot(223)
    #plt.plot(blrs)
    #plt.subplot(224)
    #plt.plot(brrs)
    #plt.show()
    
    #glrs = rayleighStretch(gl)
    #grrs = rayleighStretch(gr)
    #rlrs = rayleighStretch(rl)
    #rrrs = rayleighStretch(rr)
    
    #brs = average(b, blrs, brrs)
    #grs = average(g, glrs, grrs)
    #rrs = average(r, rlrs, rrrs)
    
    #imgcs = cv2.merge((brs, grs, rrs))
    cv2.imshow("original",img)
    cv2.imshow("rayleigh", imgcs)
    cv2.waitKey()
    
if __name__ == '__main__':
    main()