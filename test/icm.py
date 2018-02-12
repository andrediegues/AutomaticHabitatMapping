#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:04:46 2018

@author: diegues
"""

# final version of this transformation is in imageFilters.py

from matplotlib import pyplot as plt
import imageFilters as imf
import numpy as np
import sys
import cv2
import itertools as it

def linearContrastStretchingProcessing(img):
    hashmap = {}
    bot, top = min(img.ravel()), max(img.ravel())
    rmin = np.percentile(img.ravel(), 1)
    rmax = np.percentile(img.ravel(), 99)
        
    print(bot, top, rmin, rmax)
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):   
        if img[i,j] not in hashmap:
            if img[i,j] >= 0 and img[i,j] <= rmin:
                hashmap[img[i,j]] = bot/rmin * img[i,j]
                #print("bot", hashmap[img[i,j]])
            elif img[i,j] > rmax and img[i,j] <= 255:
                hashmap[img[i,j]] = (255 - top) / (255 - rmax) * (img[i,j] - rmax) + top
                #print("top", hashmap[img[i,j]])
            elif img[i,j] > rmin and img[i,j] <= rmax:
                hashmap[img[i,j]] = int(((top - bot) * (img[i,j] - rmin) / (rmax - rmin)) + bot)
                #print("TF", hashmap[img[i,j]])
    img2 = img
    for i,j in it.product(range(img.shape[0]), range(img.shape[1])):
        #if img2[i,j] in hashmap:
            #print(img2[i,j], hashmap[img2[i,j]])
            img2[i,j] = hashmap[img2[i,j]]
        
                
    return img2



def main():
    imgpath = sys.argv[1]
    img = cv2.imread(imgpath)
    rgbcs = imf.rgbStretch(imgpath)
    
    plt.figure(figsize=(24,12))
    plt.subplot(2,3,4)
    color = ('b', 'g', 'r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])    
    
    plt.subplot(2,3,5)
    for i,col in enumerate(color):
        histr2 = cv2.calcHist([rgbcs],[i],None,[256],[0,256])
        plt.plot(histr2,color = col)
        plt.xlim([0,256])
        
    plt.subplot(231), plt.imshow(plt.imread(imgpath)), plt.axis('off')
    
    hlsimg = cv2.cvtColor(rgbcs, cv2.COLOR_RGB2HLS)
    #cv2.imshow("RGB image", rgbimg)
    #cv2.imshow("HLS image", hlsimg)
    #cv2.waitKey()
    hue = hlsimg[:,:,0]
    light = hlsimg[:,:,1]
    saturation = hlsimg[:,:,2]
    #cv2.imshow("hls image", hlsimg)
    lcs = imf.linearStretch(light)
    scs = imf.linearStretch(saturation)
    
    #plt.subplot(121)
    #hist = cv2.calcHist([saturation], [0],None, [256], [0,256])
    #plt.plot(hist)
    #plt.subplot(122)
    #h2 = cv2.calcHist([lcs],[0], None, [256], [0,256])
    #plt.plot(h2)
    #plt.show()
    
    newhls = cv2.merge((hue,lcs,scs))
    readyRGB = cv2.cvtColor(newhls, cv2.COLOR_HLS2RGB)
    plt.subplot(2,3,6)
    for i,col in enumerate(color):
        histr2 = cv2.calcHist([readyRGB],[i],None,[256],[0,256])
        plt.plot(histr2,color = col)
        plt.xlim([0,256])
    plt.subplot(232), plt.imshow(cv2.cvtColor(rgbcs, cv2.COLOR_RGB2BGR)), plt.axis('off')
    plt.subplot(233), plt.imshow(cv2.cvtColor(readyRGB, cv2.COLOR_RGB2BGR)), plt.axis('off')
    #plt.savefig('histogram_differences.png')
    
    #cv2.imshow("new hls image", newhls)
    cv2.imshow("done image", readyRGB)
    cv2.waitKey()

# o azul como e predominante fazemos contrast stretching ao verde e vermelho para estar a mesma escala pelos limites do azul
# vemos como fica e avancamos

if(__name__ == "__main__"):
    main()