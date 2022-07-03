#!/usr/bin/env python

# This code it to read the sample and merged vcf first to verify if both files
# has the same positions predicted and then predict the continent for each meassurement

import pickle
from time import time

import my_constants as c
from helpers import *
from vcf import *

# read the input data
vcf_sample = vcf_reader( c.sample_file)
vcf = vcf_reader( c.prediction_output_path + "merged_file.vcf.gz")

# If both files contains the same rows then all the files to predict
# has at least all the SNPs reported in the sample file.
# If the file don't have the same lines here I need to exit with error
if len(vcf) != len(vcf_sample):
    print( "\n   At this point sample file and the input files has not the same SNPs in their content."+
    " Because the pretrained model requires the same SNPs I can't continue")
    print( "To correct this problem you can copy the files to predict also in the data ingestion folder"+
    " and remove manually the file pca.pkl and kmeans.pkl in the folder named model, and use the command 'make predict' to retrain the model.")
    raise SystemExit(1)

# Remove the aditional files
del vcf_sample
del vcf["sample"]

# Transform allels data into one hot encoding
print( "encoding data:")
start=time()
encoded_data = one_hot_encoder( vcf["ALT"].to_numpy(dtype=str), vcf.iloc[:,9:].to_numpy(dtype=str))
print(f"elapsed time: {time()-start}")

# Get the hashes involved
sources = [ src for src in vcf.columns if len(src)>8]

# Exit if number of hashes is 0
if len( sources) == 0:
    print( "\n   error on input data, to predict there must be at least one file in data/03_data_to_predict/ folder")
    raise SystemExit(1)

# Make pca transform
try:
    pca = pickle.load( open( c.pretrained_pca, "rb"))
    encoded_data = pca.transform( encoded_data.transpose())
except:
    print( f"   Error loading pca, if the files {c.pretrained_pca} and {c.pretrained_model} exists remove them and run the command again")
    raise SystemExit(1)

# Make kmeans prediction
try:
    kmeans = pickle.load( open( c.pretrained_model, "rb"))
    predictions = kmeans.predict( encoded_data)
except:
    print( f"   Error loading pca, if the files {c.pretrained_pca} and {c.pretrained_model} exists remove them and run the command again")
    raise SystemExit(1)

# Load predictor map
prediction_map = pickle.load( open( c.predictor_map, "rb"))

# Report the prediction results
print( "The results of the prediction are:\n")
for hash,prediction in zip( sources, predictions):
    print( hash, prediction_map[ prediction][0:3])

print("")