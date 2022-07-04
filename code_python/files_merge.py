#!/usr/bin/env python

# This code is to read all the vcf files and merge them in a new vcf
#
# this code uses vcf_parallel_merge to read in parallel by pairs all the
# input vcf and merge them preserving only the common SNPs for each pair.
# This process is repeated until all the files has been merged into a new
# vcf file which stores all the common SNPs and the data for each sample.

import sys
from glob import glob
from time import time

import my_constants as c
from vcf.vcf_parallel_merge import *

# Check arguments
predict = 0
for arg in sys.argv:
    if arg == "predict":
        predict = 1

# Read the complete list of vcf files
input_path = ["data/01*/*.gz","data/04*/*.gz"][predict]
input_list = glob( input_path)
input_list.sort()

# Config the new path for the output file
output_path = [c.output_path,c.prediction_output_path][predict]
output_path += "merged_file.vcf.gz"

# Start the merge process ussing all cores
init_time = time()
vcf_merge( input_list, output_path)

# Print the elapsed time
print( f"elapsed time: {time()-init_time}s")
