#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:49:27 2018

@author: diegues
"""
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.datasets import mnist

(mnist_train, mnist_train_labels), (mnist_test, mnist_test_labels) = mnist.load_data()
mnist_train = mnist_train.reshape(mnist_train.shape[0], 28, 28, 1).astype('float32') / 255
mnist_test = mnist_test.reshape(mnist_test.shape[0], 28, 28, 1).astype('float32') / 255

train_labels = keras.utils.to_categorical(mnist_train_labels, 10)
test_labels = keras.utils.to_categorical(mnist_test_labels, 10)

model = Sequential()
model.add(Conv2D(64, (4,4), activation='relu', input_shape=(28, 28, 1), padding='same'))
model.add(MaxPooling2D((2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(32, (2,2), activation='relu', padding='same'))
model.add(MaxPooling2D((2,2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(mnist_train, train_labels, epochs=10, batch_size=64)
# 35 epochs e suficiente o treino converge para 99.4 %

model.summary()

test_labels = (test_labels > .5).astype('float32')

p = model.predict(mnist_test)
p = (p > .2)
p
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(test_labels.argmax(axis=1), p.argmax(axis=1))
sum(cm.diagonal())/len(mnist_test)
score = model.evaluate(mnist_test, test_labels)
print(score) 
# [0.026451086297453252, 0.99360000000000004]

# 35 epochs e suficiente o treino converge para 99.4 %