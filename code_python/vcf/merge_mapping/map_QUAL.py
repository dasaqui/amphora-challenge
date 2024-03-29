# This function is designed to deal with the merge of QUAL
# columns, and must be run after merge the column ALT
#
#

def map_QUAL( row, sources):
    # Extract required data
    left = row['QUAL']
    right = row['QUAL_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    msg = f"Error mergin ALT: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)