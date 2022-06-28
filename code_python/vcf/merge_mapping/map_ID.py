# This function is designed to deal with the merge of ID
# columns, and must be run before all the other mappings
#
#

from operator import le


def map_ID( row, sources):
    # Extract required data
    left = row['ID']
    right = row['ID_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If one column is empty return the best option
    if( right == '.'): return left
    if( left == '.'): return right

    # If both columns are not empty merge all SNPs
    SNPs = set(left.split(";"))|set(right.split(";"))
    if all( [ "rs" ==  SNP[0:2] for SNP in SNPs]): return ";".join( SNPs)

    # If you are here, ther is an invalid SNP that must be
    # checked with caution
    msg = f"Error mergin ID: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)