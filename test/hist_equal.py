#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:44:06 2018

@author: flintswil
"""

import cv2
img = cv2.imread("/home/diegues/2018-05-01-OMARE/logs/lauv-noptilus-3/20180501/104728_cam-np3/mra/FilteredPhotos/WhiteBalance/wb_frame54.jpg")
b = img[:,:,0]
g = img[:,:,1]
r = img[:,:,2]
#he = cv2.equalizeHist(img)
heb = cv2.equalizeHist(b)
heg = cv2.equalizeHist(g)
her = cv2.equalizeHist(r)
imghe = cv2.merge((heb,heg,her))
cv2.imwrite("he.jpg", imghe)
#dst = cv2.fastNlMeansDenoisingColored(imghe, None, 10,10,7,21)
#cv2.imwrite("denoise.jpg", dst)
