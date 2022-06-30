#!/usr/bin/env python

# This code is to read all the vcf files and merge them in a new vcf

import constants as c
from vcf.vcf_parallel_merge import *
from glob import glob
import time

# Read the complete list of vcf files
input_list = glob("data/01*/*.gz")

# Config the new path for the output file
output_path = c.output_path + "merged_file.vcf.gz"

# Start the merge process ussing all cores
init_time = time()
vcf_merge( input_list, output_path)

# Print the elapsed time
print( f"elapsed time: {time()-init_time}s")