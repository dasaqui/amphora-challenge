#!/usr/bin/env python

# This file is to keep ordered aditional codes

from numba import njit
import my_constants as c
import numpy as np

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
