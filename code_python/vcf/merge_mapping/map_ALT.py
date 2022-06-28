# This function is designed to deal with the merge of ALT
# columns, and must be run after merge the column REF
#
# This tool can deal with some known details taking in consideration
# the reported data on ncbi changing each invalid register ALT data
# with "-" to be removed later.

def map_ALT( row, sources):
    # Extract required data
    left = row['ALT']
    right = row['ALT_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # Deal with known errors
    ret = ""
    if( row["CHROM"] == '10' and row["POS"] == 133479924 and "AG" in [row["ALT"],row["ALT_R"]]):
        # False insertion (rs56153029)
        ret = "-"
    elif( row["CHROM"] == '18' and row["POS"] == 76441205 and "GT" in [row["ALT"],row["ALT_R"]]):
        # False insertion (rs74749580,rs571795883)
        ret = "-"

    if( ret != ""): return ret

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    msg = f"Error mergin ALT: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)