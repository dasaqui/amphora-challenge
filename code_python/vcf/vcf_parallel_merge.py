import os
from multiprocessing import Pool, cpu_count

from .vcf_merge import vcf_merge as non_parallel_merge
from .vcf_reader import *
from .vcf_writer import *


# this function is to merge a large list of input vcf files into a
# new unified vcf using to complete this task parallel processing
def vcf_merge( input_list: list, output_file: str):
    # create a new pool to use all available cores
    pool = Pool( cpu_count())

    # get the folder to store the partial merges
    path = "/".join( output_file.split("/")[0:-1]) + "/"

    # If the list includes more than two files start an iterative
    # process to merge two by two files in parallel procecess
    counter = 1
    while len( input_list) > 2:
        # Split the list in pairs and arguments for each worker
        input_list = [input_list[ i:min(i+2,len(input_list))] for i in range( 0, len(input_list), 2)]
        arguments = [ (elements, path, counter>1) for elements in input_list]

        # call the workers
        input_list = pool.starmap( merge_worker, arguments)

        # tell the user about our partial progress
        print( f"iteration number {counter} finished, pending to merge are {len(input_list)} files")
        counter += 1
    
    # final merge
    final_path = merge_worker( input_list, output_file, rm_input=counter>1, final_path=True)
    return final_path



# this worker is to use parallel processing in the merge process
#
# to reduce the memory used each worker receives two input paths
# reads both paths, merge them in a new vcf file and saves it
# returning the new path
def merge_worker( vcf_list: list, output_path:str, rm_input = False, final_path = False):
    # verify the number of elements in the list
    if len( vcf_list) == 1: return vcf_list[0]
    elif len( vcf_list) != 2: raise Exception( "Incorrect number of input elements")

    # Split the list
    vcf1_path, vcf2_path = vcf_list

    # read paths and load into a vcf dataframe
    vcf1 = vcf_reader( vcf1_path)
    vcf2 = vcf_reader( vcf2_path)

    # merge both vcf files
    vcf = non_parallel_merge( vcf1,vcf2)

    # make a new path for the output data
    if not final_path:
        hash1 = vcf1.columns[9].split("-")[0]
        hash2 = vcf2.columns[9].split("-")[0]
        path = output_path + hash1 + "-" + hash2 + "-tmp.vcf.gz"
    else: path = output_path

    # save the new vcf, remove the old vcf and return the path
    vcf_writer( vcf, path)
    if rm_input: 
        os.remove( vcf1_path)
        os.remove( vcf2_path)
    return path



