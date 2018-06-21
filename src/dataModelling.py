#!/usr/bin/env pY_ohethon3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 11:09:20 2018

@author: diegues
"""

# data modelling

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import cv2
import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from sklearn.metrics import confusion_matrix

def printWrongPreds(preds, targets):
    df = pd.DataFrame()
    images = []
    predictions = []
    targets_ = []
    if(type(preds) == pd.DataFrame):          
        predsClass = preds.idxmax(axis=1)
        targetsClass = targets.idxmax(axis=1)  
        for i in range(0,len(predsClass)):
            if(predsClass[i] != targetsClass[i]):
                images.append(targets.index[i])
                predictions.append(predsClass[i])
                targets_.append(targetsClass[i])
                print('Image:', targets.index[i],'\t\tPrediction:', predsClass[i], '\tTarget:', targetsClass[i])
    else:
        for i in range(0,len(preds)):
            if(preds[i] != targets['EunisCode'][i]):
                images.append(targets.index[i])
                predictions.append(preds[i])
                targets_.append(targets['EunisCode'][i])
                print('Image:', targets.index[i],'\t\tPrediction:', preds[i], '\tTarget:', targets['EunisCode'][i])
    df['image'] = images
    df['prediction'] = predictions
    df['target'] = targets_
    return df


folder_path = "/home/diegues/Desktop/ProcessedImages/"
data = pd.read_csv(folder_path + "labeled_data.csv")
#classes = open(folder_path + "classes.txt", "r").readlines()

filenames = data['filename']
targets = data['EunisCode']

# one-hot encoding
targets_ohe = pd.get_dummies(data['EunisCode'])
#species_ohe = pd.get_dummies(data['species'])

# dealing with NaNs
data = data.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 
                  'AphiaID', 'EunisName', 'EunisCode', 'date', 'timestamp', 'species'],
                 axis = 1)

X = data.groupby('filename').max()
Y_ohe = pd.concat([filenames,targets_ohe], axis = 1).groupby('filename').max()
Y_cat = pd.concat([filenames,targets], axis = 1).groupby('filename').max()

print(pd.value_counts(Y_cat.EunisCode).to_frame().reset_index())

# tts
train_X_ohe, test_X_ohe, train_Y_ohe, test_Y_ohe = train_test_split(X, Y_ohe, test_size = 0.3)
train_X_cat, test_X_cat, train_Y_cat, test_Y_cat = train_test_split(X, Y_cat, test_size = 0.3)

# Random Forest prediction
rf = RandomForestClassifier(n_estimators = 100)
rf.fit(train_X_ohe, train_Y_ohe)
predictions_rf = rf.predict(test_X_ohe)
predictions_rf = pd.DataFrame(predictions_rf)
predictions_rf.columns = test_Y_ohe.columns.values
print(pd.DataFrame([(name,round(value,3)) for name,value in zip(X.columns,rf.feature_importances_)]))
print('RF:\t',rf.score(test_X_ohe, test_Y_ohe))
failed_rf = printWrongPreds(predictions_rf, test_Y_ohe)

# Support Vector Machines
svm = svm.SVC()
svm.fit(train_X_cat, train_Y_cat.values.ravel())
preds_svm = svm.predict(test_X_cat)
print('SVM:\t',accuracy_score(test_Y_cat, preds_svm))
#failed_svm = printWrongPreds(preds_svm, test_Y_cat)


# Neural Networks
## sklearn

scaler = StandardScaler()
scaler.fit(train_X_cat)

train_X_scaled = scaler.transform(train_X_cat)
test_X_scaled = scaler.transform(test_X_cat)
"""
mlp = MLPClassifier(hidden_layer_sizes=(4096,4096,1000))
mlp.fit(train_X_scaled,train_Y_cat.values.ravel())

predictions_nn = mlp.predict(test_X_scaled)
print('sklearn NN:\t',accuracy_score(test_Y_cat,predictions_nn))
failed_nn = printWrongPreds(predictions_nn, test_Y_cat)
"""
## keras

model = Sequential()
model.add(Dense(4096, activation='relu', input_dim=4))
model.add(Dropout(0.2))
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.8))
model.add(Dense(13, activation='sigmoid')) 

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(train_X_scaled, train_Y_ohe, epochs=10,validation_data=(test_X_scaled,test_Y_ohe))
predskeras_nn = pd.DataFrame(model.predict(test_X_scaled))
predskeras_nn.columns = test_Y_ohe.columns.values
score = model.evaluate(test_X_scaled, test_Y_ohe)

print('Keras NN:\t', score)
predskeras_nn = (predskeras_nn > 0.20).astype(int)
#failed_keras = printWrongPreds(predskeras_nn,test_Y_ohe)
# Image Classification

## Support Vector Machines
"""
classes = np.sort(np.array(Y_cat['EunisCode'].unique()))
class_map = dict((k,v) for (k, v) in zip(classes, [np.float32(i) for i in range(0,len(classes))]))
path_to_imgs = '/home/diegues/Desktop/ProcessedImages/LabeledData/'

X_train = []
X_test = []
y_train = []
y_test = []
i=0
for file in os.listdir(path_to_imgs):
    i = i + 1
    print(i)
    img = cv2.resize(cv2.imread(path_to_imgs + file, 0),(200,150))
    xarray_img = np.squeeze(np.array(img).astype(np.float32))
    m, v = cv2.PCACompute(xarray_img, mean = None)
    array = np.array(v)
    flat_array = array.ravel()
    if file in train_X_cat.index:
        X_train.append(flat_array)
        y_train.append(int(class_map[train_Y_cat['EunisCode'].loc[file]]))
        
    elif file in test_X_cat.index:
        X_test.append(flat_array)
        y_test.append(int(class_map[test_Y_cat['EunisCode'].loc[file]]))

X_train = np.float32(X_train)
X_test = np.float32(X_test)
y_train = np.float32(y_train)
y_test = np.float32(y_test)

img_svm = cv2.ml.SVM_create()
img_svm.setKernel(cv2.ml.SVM_LINEAR)
img_svm.setType(cv2.ml.SVM_C_SVC)
img_svm.setC(2.67)
img_svm.setGamma(5.383)
img_svm.train(X_train, cv2.ml.ROW_SAMPLE, y_train)
        
result = img_svm.predict(X_test)[1]
"""
## Convolutional Neural Networks - VGG config D

vgg16 = Sequential()

vgg16.add(Conv2D(64,(3,3),activation='relu', input_shape=(224,224,3), padding='same'))
vgg16.add(Conv2D(64,(3,3),activation='relu', padding='same'))
vgg16.add(MaxPooling2D((2,2), (2,2)))
vgg16.add(Dropout(.25))

vgg16.add(Conv2D(128,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(128,(3,3),activation='relu', padding='same'))
vgg16.add(MaxPooling2D((2,2), (2,2)))
vgg16.add(Dropout(.5))

vgg16.add(Conv2D(256,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(256,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(256,(3,3),activation='relu', padding='same'))
vgg16.add(MaxPooling2D((2,2), (2,2)))
vgg16.add(Dropout(.5))

vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(MaxPooling2D((2,2), (2,2)))
vgg16.add(Dropout(.5))

vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(Conv2D(512,(3,3),activation='relu', padding='same'))
vgg16.add(MaxPooling2D((2,2), (2,2)))
vgg16.add(Dropout(.5))

vgg16.add(Flatten())
vgg16.add(Dense(4096, activation='relu'))
vgg16.add(Dropout(0.25))
vgg16.add(Dense(4096, activation='relu'))
vgg16.add(Dropout(0.5))
vgg16.add(Dense(1000, activation='relu'))
vgg16.add(Dropout(0.75))
vgg16.add(Dense(13, activation='softmax'))

vgg16.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
vgg16.summary()

# DeepSense AI NOAA competition approach

dsaiNOAA = Sequential()

dsaiNOAA.add(Conv2D(32,(3,3),activation='relu', input_shape=(512,512,3), padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.25))

dsaiNOAA.add(Conv2D(64,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.25))

dsaiNOAA.add(Conv2D(64,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(Conv2D(128,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(Conv2D(128,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.25))

dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.25))

dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.5))

dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(Conv2D(256,(3,3),activation='relu', padding='same'))
dsaiNOAA.add(MaxPooling2D(pool_size=(3,3), strides=(2,2)))
dsaiNOAA.add(Dropout(.5))

dsaiNOAA.add(Flatten())
dsaiNOAA.add(Dense(256, activation='relu'))
dsaiNOAA.add(Dense(64, activation='relu'))
dsaiNOAA.add(Dense(13, activation='softmax'))

dsaiNOAA.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
dsaiNOAA.summary()