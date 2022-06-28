# This function is designed to deal with the merge of FORMAT
# columns, and must be run after merge the column INFO
#
#

def map_FORMAT( row, sources):
    # Extract required data
    left = row['FORMAT']
    right = row['FORMAT_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    raise Exception( f"error mergin FORMAT: {left}!={right}")