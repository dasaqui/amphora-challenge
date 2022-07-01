#!/usr/bin/env python

# This file is to keep ordered aditional codes

from numba import njit
import my_constants as c
import numpy as np

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
