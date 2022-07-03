#!/bin/bash

#####
# This file is to create a sample file from the merged file to
# be used at the prediction process

INPUT_FILE="data/02_merged_data/merged_file.vcf.gz"
OUTPUT_FILE="data/04_prediction_preprocessed/sample.vcf"

AWK_CODE="code_awk/vcf2sample.awk"

zcat $INPUT_FILE | awk -F $'\t' -f $AWK_CODE > $OUTPUT_FILE

gzip $OUTPUT_FILE -f
