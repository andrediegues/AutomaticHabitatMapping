#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:22:23 2018

@author: diegues
"""
import cv2
from skimage import data
from skimage.restoration import denoise_wavelet

# /home/diegues/wreck/mra/filtered_sss_images/filtered_sss_1.png

img = data.imread('/home/diegues/madeira14/mra/ICM/icm_filtered_sss_1.png')
#print(img[5])
denoised = denoise_wavelet(img, sigma = .01, wavelet='db1') # doesnt work
#print(denoised[5])
cv2.imshow('original', img)
cv2.imshow('wavelet', denoised)
cv2.waitKey()
