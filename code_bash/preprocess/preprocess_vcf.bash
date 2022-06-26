#!/bin/bash

#####
# This code is to preprocess one vcf file
#
# This preprocessing involves format verification to read correctly
# each file compressed or not. 
#
# The output vcf file will be sorted in dictionary order by chromosome
# and position, and will be updated this change in the metadata
