#!/usr/bin/env python

# This code is to deal with KMeans clustering an to evaluate the process between multiple
# executions of kmeans.

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
    # prediction_map_keys:   predicted class -> real class number
    # prediction_map_code:   predicted class -> real class code UNDERSCORE predicted class key
    prediction_map_keys = {i:0 for i in set( labels[ "prediction"])}
    prediction_map_code = {i:"???_"+str(i) for i in range( k)}
    for key in prediction_map_keys:
        # set of real classes in current predicted class
        population_code = labels["Superpopulation code"][ labels[ labels[ "prediction"] == key].index]
        population_code = population_code.to_list()

        # Detect the most frequent code and use it to map the class
        population_code = max(set(population_code), key = population_code.count)
        prediction_map_keys[ key] = labels_dict[ population_code]
        prediction_map_code[ key] = population_code + "_" + str( key)

    # Make a confusion matrix over labeled data
    confusion_matrix = np.zeros( (len( labels_dict), len( labels_dict)))
    for i in range( labels.shape[0]):
        # Get the bin for current element on labels
        real = labels_dict[ labels.iloc[i,1]]
        pred = prediction_map_keys[ labels.iloc[i,2]]

        # Update current bin
        confusion_matrix[ real, pred] += 1

    # assing new classes for predicted data
    labels["prediction"] = np.array( [ prediction_map_code[key] for key in labels["prediction"]])
    unlabeled["prediction"] = np.array( [ prediction_map_code[key] for key in unlabeled["prediction"]])

    # Save model
    if not os.path.exists( c.pretrained_model):
        pickle.dump( kmeans, open( c.pretrained_model, "wb"))

    return labels, unlabeled, confusion_matrix, labels_dict
