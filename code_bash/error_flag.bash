#!/bin/bash

#####
# This script is only to indicate the precense of an error while
# processing some data
#
# The error is indicated as a text file that stores some relevant information to 
# keep track of the event and solve it.
#
#
# The script requires three arguments: calling_script, source_file, message
#   calling_script: is the script running while the error was detected
#   source_file: is the file being processed while the error was detected
#   message: is some aditional information useful to find the error
#
#
# The output is a file named error_flag.err and is a text file

OUTPUT_FILE="error_flag.err"

# check that there is at least one parameter, if not stops the script
[[ $# -eq 0 ]] && $( 
    date >> $OUTPUT_FILE
    echo "$0 called without arguments" >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
    exit 1
    )

# First message so stor (caller script)
date >> $OUTPUT_FILE
echo "  called by '${$1}'" >> $OUTPUT_FILE
