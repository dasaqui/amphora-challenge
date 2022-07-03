#!/bin/bash

#####
# This code is to preprocess one csv file
#
# This preprocessing code trust that the format is really a valid csv
#
# The output vcf file will be sorted in dictionary order by chromosome
# and position, and will be logged this change in the metadata

# Checking that there is one or two argument and exit if not
[[ $# -lt 1 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -lt 1 ]] && bash "code_bash/error_flag.bash" "$0" "null" "Called without arguments"
[[ $# -lt 1 ]] && exit 7
[[ $# -gt 2 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -gt 2 ]] && bash "code_bash/error_flag.bash" "$0" "null" "Called without arguments"
[[ $# -gt 2 ]] && exit 7

# Change paths if there is a second argument
if [[ "$2" == "predict" ]]
then
   INPUT_FOLDER="03_data_to_predict"
   OUTPUT_FOLDER="04_prediction_preprocessed"
else
   INPUT_FOLDER="00_data_ingestion"
   OUTPUT_FOLDER="01_preprocessed_data"
fi

# output filename not gziped
input="$1"
output=$( echo "$1"| sed "s/${INPUT_FOLDER}/${OUTPUT_FOLDER}/g"| sed "s/\.csv/\.csv\.vcf/g")
id_hash=$( echo "$1"| sed "s/.*\///g"| sed "s/\.csv//g")

# date to be stored in the metadata
meta=$(date +%Y%M%d)

#########################
# This line is only to correct a detected error on chomosome 2 position 236072830
#    the second alternative allel should be G not TT
correction1="s/2;236072830,GT,TT,TT/2;236072830,GT,TT,G/"

# output data splitting by chromosome
cat "${input}" |\
sed "${correction1}" |\
sed "s/;/,/g" |\
awk -v meta="${meta}" -v output="${output}" -v id_hash="${id_hash}" -f "code_awk/csv2vcf.awk"

# Data merging and sorting
for chromosome in {1..23}
do
    # Check if there is a file for this chromosome
    [[ -f "${output}_${chromosome}" ]] || continue

    # this pipeline will search for each chromosome in order and sort by position
    cat "${output}_${chromosome}" |\
    sort -n -k 2 >> "$output"

    # removes the temporal file
    rm "${output}_${chromosome}"
done

gzip -f "${output}"
