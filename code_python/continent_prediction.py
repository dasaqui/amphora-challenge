#!/usr/bin/env python

# This code it to read the merged vcf, split it into training and validation datasets
# and make predictions about the classes/continents for each resgister

import os.path
from time import time

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

import my_constants as c
from helpers import *
from vcf import vcf_reader

# Read the merged vcf
vcf_train = vcf_reader( c.output_path + "merged_file.vcf.gz")

# Make a vcf copy
vcf_validate = pd.DataFrame.copy( vcf_train.iloc[:,0:9], deep=True)

# Read the classes for labeled data and sort it by label
labels = pd.read_csv( c.labels_path, delimiter="\t")
labels = labels.sort_values( "Superpopulation code").reset_index(drop=True)
index_to_remove = []

# Move the validation data
for id,UUID in enumerate( labels["UUID"]):
    try:
        vcf_validate[UUID] = vcf_train[UUID]
        del vcf_train[UUID]
        vcf_validate = vcf_validate.copy()
    except:
        index_to_remove.append(id)
        print( f"id:{id}, register hash {UUID} was not found")

# Remove unused data UUIDs
labels = labels.drop( index_to_remove).reset_index( drop=True)

# Transform allels data into one hot encoding
print( "encoding data:")
start=time()
encoded_train = one_hot_encoder( vcf_train["ALT"].to_numpy(dtype=str), vcf_train.iloc[:,9:].to_numpy(dtype=str))
encoded_validate = one_hot_encoder( vcf_validate["ALT"].to_numpy(dtype=str), vcf_validate.iloc[:,9:].to_numpy(dtype=str))
print(f"elapsed time: {time()-start}")

# Implementing PCA to reduce the dimensionality of this problem
pca = PCA(500)
encoded_train = pca.fit_transform( encoded_train.transpose())
encoded_validate = pca.transform( encoded_validate.transpose())

# Kmeans evaluation over multiple repetitions
avg,std = multiple_kmeans(5, 8, encoded_train, encoded_validate, labels)
print( f"This method shows an average f1 score of {avg} and variance of {std}")

# Implementing KMeans to make class inference
if os.path.exists( c.pretrained_model):
    labels, unlabeled, confusion_matrix, labels_dict = kmeans_eval( 8, encoded_train, encoded_validate, labels, pretrained=c.pretrained_model)
else:
    labels, unlabeled, confusion_matrix, labels_dict = kmeans_eval( 8, encoded_train, encoded_validate, labels)

# Model evaluation
macro_F1, F1 = macro_F1_score( confusion_matrix)

# class accuracy and data visualization
fig = plt.figure()

plot_by( fig, (2,2,1), encoded_validate, labels, "Superpopulation code", "Labeled data")
plot_by( fig, (2,2,2), encoded_validate, labels, "prediction", "Prediction on labeled data")
plot_by( fig, (2,2,3), encoded_train, unlabeled, "prediction", "Prediction on unlabeled data")
plot_F1( fig, (2,2,4), macro_F1, F1, labels_dict)
try: plt.show()
except: pass

# save the graphs
print("Saving images")
plot_by( plt.figure(), (1,1,1), encoded_validate, labels, "Superpopulation code", "Labeled data")
plt.savefig( c.output_dir+"01_labeled_data.png")
plot_by( plt.figure(), (1,1,1), encoded_validate, labels, "prediction", "Prediction on labeled data")
plt.savefig( c.output_dir+"02_prediction_on_labeled_data.png")
plot_by( plt.figure(), (1,1,1), encoded_train, unlabeled, "prediction", "Prediction on unlabeled data")
plt.savefig( c.output_dir+"03_prediction_on_unlabeled_data.png")
plot_F1( plt.figure(), (1,1,1), macro_F1, F1, labels_dict)
plt.savefig( c.output_dir+"04_F1_score_by_group.png")

print("")
