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

# Checking that there one or two argument and exit if not
[[ $# -lt 1 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -lt 1 ]] && exit 4
[[ $# -gt 2 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -gt 2 ]] && exit 4

# Change paths if there are a second argument
if [[ "$2" == "predict" ]]
then
   path="data\/03_data_to_predict\/"
else
   path="data\/00_data_ingestion\/"
fi

# Checking the path and extension of the source file
extension="\(csv\|vcf\|vcf\.gz\)"
pathern="${path}.*${extension}"
[[ -n $( echo "$1"| sed "s/${pathern}//g") ]] && bash code_bash/error_flag.bash "$0" "$1" "pathern or extension error:
        expected path: '$( echo ${path} |sed s/\\\\//g)'
        expected extension: $( echo ${extension} |sed s/\\\\//g) in lower case"
[[ -n $( echo "$1"| sed "s/${pathern}//g") ]] && exit 5

# Checking file existence, if doesn't exists log it
[[ ! -f "$1" ]] && bash code_bash/error_flag.bash "$0" "$1" "the file doesn't exists"
[[ ! -f "$1" ]] && exit 6

# Processing tsv data
format=$( echo "$1"| sed "s/.*\(csv\)/csv/g")
[[ "$format" = "csv" ]] && bash "code_bash/preprocess/preprocess_csv.bash" "$1" "$2"
[[ "$format" = "csv" ]] && exit 0

# Processing vcf data
format=$( echo "$1"| sed "s/.*\(vcf\|vcf\.gz\)/vcf/g")
[[ "$format" = "vcf" ]] && bash "code_bash/preprocess/preprocess_vcf.bash" "$1" "$2"
[[ "$format" = "vcf" ]] && exit 0
