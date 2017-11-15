#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:03:12 2017

@author: diegues


"""
import sys
import os
import cv2
import imageFilters


def main(option, imgpath):
    if len(sys.argv) < 2:
        print("ERROR: not enough arguments")
        sys.exit(1)
    if not os.path.exists(os.path.abspath(imgpath)):
        print("ERROR: image doesn't exist")
        sys.exit(1)
    img = cv2.imread(imgpath, 0)
    if option == '--red':
        pass
    elif option == '--blue':
        pass
    elif option == '--green':
        pass
    elif option == '--negative':
        pass
    elif option == '--drm':
        pass
    elif option == '--powerstretch':
        pass
    elif option == '--linearstretch':
        img  = imageFilters.linearStretch(img)
    
    cv2.imshow("linear stretch", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
