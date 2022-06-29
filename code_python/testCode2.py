from vcf.vcf_parallel_merge import *
import constants as c
from time import time
from glob import glob

# Test for parallel code

input_list = glob("data/01*/*.gz")
input_list = [ element for index,element in enumerate( input_list) if index<1024]

init_time = time()
new_path = vcf_merge( input_list, c.output_path + "file1.vcf.gz")
print( f"new file: {new_path}")

print( f"elapsed time: {time()-init_time}s")

print( "end")
