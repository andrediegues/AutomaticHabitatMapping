#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:58:32 2018

@author: diegues
"""

from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.datasets import cifar10
from keras.models import Sequential
from keras.utils import to_categorical


(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = x_train.reshape(x_train.shape[0], 32,32,3).astype('float32')/255
x_test = x_test.reshape(x_test.shape[0], 32,32,3).astype('float32')/255

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

model = Sequential()

model.add(Conv2D(16,(3,3),padding='same', input_shape = (32,32,3), activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Dropout(.25))

model.add(Conv2D(64,(3,3),padding='same', activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Dropout(.5))

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])

model.fit(x = x_train, y = y_train, epochs = 40)

score = model.evaluate(x = x_test, y = y_test)
model.metrics_names
print('(loss, acc)\n' + str(score))