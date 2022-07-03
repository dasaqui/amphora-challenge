#!/bin/bash

#####
# This code is to preprocess one vcf file
#
# This preprocessing involves format verification to read correctly
# each file compressed or not. 
#
# The output vcf file will be sorted in dictionary order by chromosome
# and position, and will be updated this change in the metadata

# Checking that there is only one argument and exit if not
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

# input format verification
file_format=$( file "$1"| sed "s/.*(VCF).*/VCF/"| sed "s/.*(BGZF;.*/GZ/")

# selecting the correct reader tool
reader_command="null"
[[ $file_format = "GZ" ]] && reader_command="zcat"
[[ $file_format = "VCF" ]] && reader_command="cat"

# error managing
[[ $reader_command == "null" ]] && bash "code_bash/error_flag.bash" "$0" "$1" "Incorrect input file format (${file_format})"
[[ $reader_command == "null" ]] && exit 8

# output filename not gziped
input="$1"
output=$( echo "$1"| sed "s/${INPUT_FOLDER}/${OUTPUT_FOLDER}/g"| sed "s/\.gz//g")

# message to store as a part of the metadata
meta="##amphora_challenge= file sorted by chromosome and position on $(date)"

# pipeline to copy all the headers (replacing output file)
${reader_command} "$input" |\
awk -F "\t" -v output="$output" "/^#/ {print \$0 > output; next}; NF > 1 {print \$0 > output\"_\"\$1}"

# Sort by chromosome and position for each chromosome
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
