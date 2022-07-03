#!/bin/bash

#####
# This code is to list all the source files that have not been 
# preprocessed
#
# This code does not require input arguments, but will read the
# "data ingestion" folder to check one by one each file and test
# if it has been preprocessed.
# 
# If a file has not been preprocessed calls the make command to
# start the preprocessing of this file.

# select input data and confirm output folder
if [[ "$1" == "predict" ]]
then
    INPUT_FOLDER="data/03_data_to_predict/"
    OUTPUT_FOLDER="data/04_prediction_preprocessed/"
else
    INPUT_FOLDER="data/00_data_ingestion/"
    OUTPUT_FOLDER="data/01_preprocessed_data/"
fi

# reads the source folder for a complete list of files
INPUT_LIST=$(ls ${INPUT_FOLDER}*csv ${INPUT_FOLDER}*gz| sed "s/.*\///g")

# Iterate over the complete list of files
for file in $INPUT_LIST
do 
    # check the extension of the file
    [[ "${file}" == *csv ]] && ends_with_csv="yes" || ends_with_csv="no"

    # determine the output name
    [[ "${ends_with_csv}" == "yes" ]] && output="${file}.vcf.gz" || output="${file}"

    # If the file is on the preprocessed folder continue with the next file
    [[ -f "${OUTPUT_FOLDER}${output}" ]] && continue

    # To use parallel processing wait for a free thread if all the 
    # cores are busy, keeping a max queue of 100
    while [[ 100 -le $( jobs| wc -l) ]]
    do
        # sleep while the cores are busy 
        sleep 1
    done

    # At this point the file has not been processed, so start this processing
    make "${OUTPUT_FOLDER}${output}" >/dev/null &
done

# wait for all the jobs to complete
wait $(jobs -p)
