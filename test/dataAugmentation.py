#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 10:27:40 2018

@author: diegues
"""

from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.models import Sequential
from keras.utils import to_categorical

# data loading 

# data preprocessing
    # put labels to_categorical
    # use ImageDataGenerator to use data augmentation

# cnn model
model = Sequential()

# get subimages with 100x100 with convolutions

model.add(Conv2D(32, (5,5), strides=(2,1), padding="same", input_shape=(2000,1000,3), activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(rate=0.25))

model.add(Conv2D(256, (5,5), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(5,5)))
model.add(Dropout(rate=0.25))

# flatten the kernels of 100x100 to 1D to feed the NN 

model.add(Flatten())
model.add(Dense(8, activation="sigmoid"))
model.summary()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# fit the data to the model
# predict
#
