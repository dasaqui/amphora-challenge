from vcf import *
from time import time
from glob import glob

# Test for non parallel code

input_list = glob("data/01*/*.gz")
input_list = [input_list[ i:min(i+2,len(input_list))] for i in range( 0, len(input_list), 2) if i < 20]

init_time = time()
for file_couple in input_list:
    vcf1 = vcf_reader( file_couple[0])
    vcf2 = vcf_reader( file_couple[1])
    vcf = vcf_merge( vcf1, vcf2)
    hash1 = file_couple[0].split("/")[-1].split("-")[0]
    hash2 = file_couple[1].split("/")[-1].split("-")[0]
    vcf_writer( vcf, f"data/02_merged_data/{hash1}-{hash2}-tmp.vcf.gz")

print( f"elapsed time: {time()-init_time}s")

print( vcf.head())
