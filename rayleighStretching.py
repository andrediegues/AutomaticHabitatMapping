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
from scipy.stats import rayleigh

def splitHist(img):
    rmin = min(img.ravel())
    rmax = max(img.ravel())
    rmid = math.floor((rmax - rmin) / 2 + rmin)
    pixels = list(set(sorted(img.ravel())))
    l = pixels[:len(pixels) - pixels[::-1].index(rmid)]
    r = pixels[len(pixels) - pixels[::-1].index(rmid):]
    return l, r

def rayleighStretch(pixels):
    h = {}
    bot = min(pixels)
    top = max(pixels)
    for pixel in pixels:
        val = rayleigh.pdf((255 * ((pixel - bot) / (top - bot))))
        h[pixel] = val
        print(val)
    return h

def merge(img, l, r):
    imgrs = img
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        if img[i,j] in l:
            imgrs[i,j] = l[img[i,j]]
        elif img[i,j] in r:
            imgrs[i,j] = r[img[i,j]]            
    return imgrs

def main():
    imgname = sys.argv[1]
    img = cv2.imread(imgname)
    b = imf.bluefilter(imgname)
    g = imf.greenfilter(imgname)
    r = imf.redfilter(imgname)
    
    bl, br = splitHist(b)
    gl, gr = splitHist(g)
    rl, rr = splitHist(r)
    
    blrs = rayleighStretch(bl)
    brrs = rayleighStretch(br)
    glrs = rayleighStretch(gl)
    grrs = rayleighStretch(gr)
    rlrs = rayleighStretch(rl)
    rrrs = rayleighStretch(rr)
    
    brs = merge(b, blrs, brrs)
    grs = merge(g, glrs, grrs)
    rrs = merge(r, rlrs, rrrs)
    
    imgcs = cv2.merge((brs, grs, rrs))
    cv2.imshow("original",img)
    cv2.imshow("rayleigh", imgcs)
    cv2.waitKey()
    
if __name__ == '__main__':
    main()