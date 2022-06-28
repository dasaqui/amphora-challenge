def map_ID( row, sources):
    # Extract required data
    left = row['ID']
    right = row['ID_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If one column is empty return the best option
    if( right == '.'): return left
    if( left == '.'): return right

    # If both columns are not empty but are diferent we
    # shold take an action to correct it
    msg = f"Error mergin ID: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)