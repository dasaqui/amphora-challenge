#!/usr/bin/env python

# This file is to keep ordered aditional codes

import os.path
import pickle

import my_constants as c
import numpy as np
from sklearn.cluster import KMeans

from .score import macro_F1_score


def multiple_kmeans( tests, k, train, validate, labels):
    # Prepare the output data
    F1_hist = np.zeros( tests)

    # evaluate multiple times
    for i in range( tests):
        l,u,confusion,d = kmeans_eval( k, train, validate, labels)
        mF1,F1 = macro_F1_score( confusion)
        F1_hist[i] = mF1
    
    # Estimate average and variance
    avg = sum( F1_hist) / tests
    std = sum( [F1 ** 2 for F1 in F1_hist]) / tests - avg ** 2

    return avg,std

def kmeans_eval( k, train, validate, labels, pretrained=False):
    # Model trainning and predictions
    if pretrained:
        kmeans = pickle.load( open( pretrained, "rb"))
        train = kmeans.predict( train)
        validate = kmeans.predict( validate)
    else:
        kmeans = KMeans(k)
        train = kmeans.fit_predict( train)
        validate = kmeans.predict( validate)

    # Labeling the output data
    labels["prediction"] = validate
    unlabeled = {"prediction": train}

    # get a dictionary of labels
    labels_dict = { l:i for i,l in enumerate( set( labels[ "Superpopulation code"]))}

    # Map the prediction to the real class
    prediction_map = {i:0 for i in set( labels[ "prediction"])}
    for key in prediction_map:
        # set of real classes in current predicted class
        s = labels["Superpopulation code"][ labels[ labels[ "prediction"] == key].index]
        s = s.to_list()

        # Detect the most frequent code and use it to map the class
        s = max(set(s), key = s.count)
        prediction_map[ key] = labels_dict[ s]

    # Make a confusion matrix
    confusion_matrix = np.zeros( (len( labels_dict), len( labels_dict)))
    for i in range( labels.shape[0]):
        # Get the bin for current element on labels
        real = labels_dict[ labels.iloc[i,1]]
        pred = prediction_map[ labels.iloc[i,2]]

        # Update current bin
        confusion_matrix[ real, pred] += 1

    # Save model
    if not os.path.exists( c.pretrained_model):
        pickle.dump( kmeans, open( c.pretrained_model, "wb"))

    return labels, unlabeled, confusion_matrix, labels_dict
