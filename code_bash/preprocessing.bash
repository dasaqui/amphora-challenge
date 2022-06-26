#!/bin/bash

#####
# This file is to preprocess one file at data_ingestion and move it to preprocessed_data
#
# in this process the file should be changed to correct format acording to the original format
#
# there is only one argument that represents the incoming file that should be converted to vcf,
# and the correct script should be called acording to the incoming format.
#
# the output file is stored in preprocessed_data in vcf format. If there is an error the
# script should call error_flag and exit with error 

# Checking that there is only one argument and exit if not
[[ $# -ne 1 ]] && $(
    bash code_bash/error_flag.bash $0 null "script called with '$#' arguments"
    ) && exit 4

