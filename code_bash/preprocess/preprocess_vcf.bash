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
[[ $# -ne 1 ]] && bash code_bash/error_flag.bash "$0" null "script called with '$#' arguments"
[[ $# -ne 1 ]] && bash "code_bash/error_flag.bash" "$0" "null" "Called without arguments"
[[ $# -ne 1 ]] && exit 7

# input format verification
file_format=$( file "$1"| sed "s/.*(VCF).*/VCF/"| sed "s/.*(BGZF;.*/GZ/")

# selecting the correct reader tool
reader_command="null"
[[ $file_format = "GZ" ]] && reader_command="zcat"
[[ $file_format = "VCF" ]] && reader_command="cat"

# error managing
[[ $reader_command == "null" ]] && bash "code_bash/error_flag.bash" "$0" "$1" "Incorrect input file format (${file_format})"
[[ $reader_command == "null" ]] && exit 8
