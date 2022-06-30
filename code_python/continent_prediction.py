#!/usr/bin/env python

# This code it to read the merged vcf, split it into training and validation datasets
# and make predictions about the classes/continents for each resgister

from vcf import vcf_reader
import constants as c
import numpy as np
import pandas as pd
from helpers import *
from time import time

# Read the merged vcf
vcf_train = vcf_reader( c.output_path + "merged_file.vcf.gz")

# Make a vcf copy
vcf_validate = vcf_train.iloc[:,0:9]

# Read the classes for labeled data and sort it by label
labels = pd.read_csv( c.labels_path, delimiter="\t")
labels = labels.sort_values( "Superpopulation code")

# Move the validation data
for UUID in labels["UUID"]:
    try:
        vcf_validate[UUID] = vcf_train[UUID]
        del vcf_train[UUID]
    except:
        print( f"register hash {UUID} was not found")

# Transform allels data into one hot encoding
print( "encoding data:")
start=time()
encoded_train = one_hot_encoder( vcf_train["ALT"].to_numpy(dtype=str), vcf_train.iloc[:,10:].to_numpy(dtype=str))
encoded_validate = one_hot_encoder( vcf_train["ALT"].to_numpy(dtype=str), vcf_train.iloc[:,10:].to_numpy(dtype=str))
print(f"elapsed time: {time()-start}")
print("")