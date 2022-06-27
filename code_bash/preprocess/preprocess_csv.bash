#!/bin/bash

#####
# This code is to preprocess one csv file
#
# This preprocessing code trust that the format is really a valid csv
#
# The output vcf file will be sorted in dictionary order by chromosome
# and position, and will be logged this change in the metadata

# Checking that there is only one argument and exit if not
[[ $# -ne 1 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -ne 1 ]] && bash "code_bash/error_flag.bash" "$0" "null" "Called without arguments"
[[ $# -ne 1 ]] && exit 7

# output filename not gziped
input="$1"
output=$( echo "$1"| sed "s/00 data ingestion/01 preprocessed data/g"| sed "s/\.csv/\.csv\.vcf/g")
