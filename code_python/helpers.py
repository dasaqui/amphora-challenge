#!/usr/bin/env python

# This file is to keep ordered aditional codes

from numba import njit
import numba
import my_constants as c
import numpy as np
from sklearn.cluster import KMeans

# one_hot_encoder is a code to encode allel data using something similar
# to the one hot encoding. In this version if both copies of the genome 
# are equal, the result is a one hot encode data, but if they are not 
# equal the result is half step in each direction.
#
# by example: for two allels
# 0|0 -> [0]
# 1|1 -> [1]
# 0|1 and 1|0 -> [0.5]
#
# for three allels
# 0|0 -> [0,0]
# 1|1 -> [1,0]
# 2|2 -> [0,1]
# 0|1 and 1|0 -> [0.5,0]
# 0|2 and 2|0 -> [0,0.5]
# 1|2 and 2|1 -> [0.5,0.5]
#
# This code requires a complete copy of the column ALT to detect the number
# of allels present and each measure to encode it.
# @njit
def one_hot_encoder( ALT, DATA):
    # counter for the required encodings
    counter = 0

    # iterates over all the alternative allels to estimate the required array
    # to store the output data
    for index,allels in enumerate( ALT):
        # check the number of allels
        number = len( allels.split(",")) 
        if number > 2: raise Exception( c.one_hot_error)

        # counter update
        counter += number

    # allocate memory to store the output data
    encoded = np.zeros( (counter, DATA.shape[1]))

    # reset the counter
    counter = 0

    # Iterate over the complete array to generate the encoded data
    for index1,allels in enumerate( ALT):
        # check the number of allels
        number = len( allels.split(",")) 
        if number > 2: raise Exception( c.one_hot_error)

        # Encode all the data for current SNP
        encoded[counter:counter+number,:] = snp_encoder( number, DATA[index1,:])

        # counter update
        counter += number

    # return the encoded matrix
    return encoded


# Given a row of samples for an specific chrom/pos, encode the data using an
# arra with "number" of rows acording to the above description.
# @njit
def snp_encoder( number, samples_row):
    # Pre-allocate memory
    row = np.zeros( (number, len(samples_row)))

    if number == 1:
        # If this chrom/pos has only two allels do:
        for index,sample in enumerate( samples_row):
            # not necesary case, because the given sample is alredy labeled as 0
            # if sample == "0|0": row[index] = 0
            if sample == "0|0": continue

            if sample == "1|1": row[0,index] = 1
            elif sample == "0|1": row[0,index] = 0.5
            elif sample == "1|0": row[0,index] = 0.5
    else:
        # If there are three allels do:
        for index,sample in enumerate( samples_row):
            # not necesary case, because the given sample is alredy labeled as 0
            # if sample == "0|0": row[0:2,index] = [0,0]
            if sample == "0|0": continue

            if sample == "1|1": row[0,index] = 1
            elif sample == "2|2": row[1,index] = 1
            elif sample == "0|1": row[0,index] = 0.5
            elif sample == "1|0": row[0,index] = 0.5
            elif sample == "0|2": row[1,index] = 0.5
            elif sample == "2|0": row[1,index] = 0.5
            elif sample == "2|1": row[0:2,index] = [0.5,0.5]
            elif sample == "1|2": row[0:2,index] = [0.5,0.5]
    
    # return the encoded data
    return row


# plot_by is a helper code to plot given data grouped by a condition in a
# 3d Scattered plot
def plot_by( fig, index, pca_data, labels, group_by, title=""):
    # Prepare the grid
    if len( index) == 3:
        rows,cols,index = index
    else:
        rows,cols = (1,2)
    ax = fig.add_subplot(rows,cols,index,projection='3d')

    # Plot by group
    groups = set( labels[ group_by])
    for group in groups:
        # Split data by superpopulation
        rows = [number for number,code in enumerate( labels[group_by]) if code == group]

        # get the coordinates for each point
        xs = pca_data[ rows, 0]
        ys = pca_data[ rows, 1]
        zs = pca_data[ rows, 2]

        ax.scatter( xs, ys, zs)

    # Labels and legends
    ax.legend( [k for k in groups])
    ax.set_xlabel("first component")
    ax.set_ylabel("second component")
    ax.set_zlabel("third component")

    # Write a title
    if title != "": ax.set_title( title)


def multiple_kmeans( tests, k, train, validate, labels):
    # Prepare the output data
    F1_hist = np.zeros( tests)

    # evaluate multiple times
    for i in range( tests):
        l,u,confusion = kmeans_eval( k, train, validate, labels)
        mF1,F1 = macro_F1_score( confusion)
        F1_hist[i] = mF1
    
    # Estimate average and variance
    avg = sum( F1_hist) / tests
    std = sum( [F1 ** 2 for F1 in F1_hist]) / tests - avg ** 2

    return avg,std

def kmeans_eval( k, train, validate, labels):
    # Implementing KMeans to make class inference
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

    return labels, unlabeled, confusion_matrix


def macro_F1_score( confusion_matrix):
    # Prepare all the elements to estimate precision
    categories = confusion_matrix.shape[0]
    precision = []
    recall = []

    # Iterate over all classes
    for cat in range( categories):
        # Prepare needed vars
        TP = 0
        TN = 0
        FP = 0
        FN = 0

        for i,j in [[i,j] for i in range(categories) for j in range(categories)]:
            if cat == j:
                if i == cat:
                    # True positive
                    TP += confusion_matrix[i,j]
                else:
                    # False positive
                    FP += confusion_matrix[i,j]
            else:
                if i == cat:
                    # False negative
                    FN += confusion_matrix[i,j]
                else:
                    # True negative
                    TN += confusion_matrix[i,j]

        # metrics estimation
        precision.append( TP / (TP+FP))
        recall.append( TP / (TP + FN))

    # F1 score
    F1 = [2 * p * r / (p + r) for p,r in zip( precision, recall)]
    macro_p = sum( precision) / len( precision)
    macro_r = sum( recall) / len( recall)
    macro_F1 = 2 * macro_p * macro_r / (macro_p + macro_r)

    return macro_F1, F1
