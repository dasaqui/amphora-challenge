def map_REF( row, sources):
    # Extract required data
    left = row['REF']
    right = row['REF_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    msg = f"Error mergin REF: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)