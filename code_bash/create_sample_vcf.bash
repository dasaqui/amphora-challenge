#!/bin/bash

#####
# This file is to create a sample file from the merged file to
# be used at the prediction process

# Some constants
INPUT_FILE="data/02_merged_data/merged_file.vcf.gz"
OUTPUT_FILE="data/04_prediction_preprocessed/00000000-sample.vcf"

# The code to process the input merged file
AWK_CODE="code_awk/vcf2sample.awk"

# File unzipping and processing
zcat $INPUT_FILE | awk -F $'\t' -f $AWK_CODE > $OUTPUT_FILE

# Zip output file
gzip $OUTPUT_FILE -f
