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
    bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
    ) && exit 4

# Checking the path and extension of the source file
path="data\/00 data ingestion\/"
extension="\(csv\|vcf\|vcf\.gz\)"
pathern="${path}.*${extension}"
[[ -n $( echo "$1"| sed "s/${pathern}//g") ]] && $(
    bash code_bash/error_flag.bash "$0" "$1" "pathern or extension error:
        expected path: '$( echo ${path} |sed s/\\\\//g)'
        expected extension: $( echo ${extension} |sed s/\\\\//g) in lower case"
    ) && exit 5