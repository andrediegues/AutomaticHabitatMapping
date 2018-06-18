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


folder_path = "/home/diegues/Desktop/ProcessedImages/"
data = pd.read_csv(folder_path + "labeled_data.csv")
#classes = open(folder_path + "classes.txt", "r").readlines()

filenames = data['filename']
targets = data['EunisCode']

# one-hot encoding
targets_ohe = pd.get_dummies(data['EunisCode'])
species_ohe = pd.get_dummies(data['species'])

# dealing with NaNs
data = data.drop(['roll', 'pitch', 'level1', 'level2', 'level3', 'level4', 'level5', 'level6', 
                  'AphiaID', 'EunisName', 'EunisCode', 'date', 'timestamp', 'species'],
                 axis = 1)

X = pd.concat([data,species_ohe], axis = 1).groupby('filename').max()
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
print('RF:\t',rf.score(test_X_ohe, test_Y_ohe))
print(pd.DataFrame([(name,round(value,3)) for name,value in zip(X.columns,rf.feature_importances_)]))

# Support Vector Machines
svm = svm.SVC()
svm.fit(train_X_cat, train_Y_cat.values.ravel())
preds_svm = svm.predict(test_X_cat)
print('SVM:\t',accuracy_score(test_Y_cat, preds_svm))

# Neural Networks
scaler = StandardScaler()
scaler.fit(train_X_cat)

train_X_scaled = scaler.transform(train_X_cat)
test_X_scaled = scaler.transform(test_X_cat)

mlp = MLPClassifier(hidden_layer_sizes=(64,64,128))
mlp.fit(train_X_scaled,train_Y_cat.values.ravel())

predictions_nn = mlp.predict(test_X_scaled)
print('NN:\t',accuracy_score(test_Y_cat,predictions_nn))
