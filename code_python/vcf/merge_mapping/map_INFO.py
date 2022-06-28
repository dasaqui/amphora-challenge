# This function is designed to deal with the merge of INFO
# columns, and must be run after merge the column FILTER
#
# this tool can deal with up to three allels and is pending
# a correction if both register report diferent number of
# allels.

def map_INFO( row, sources):
    # exit if is an invalid row
    if( row['ALT_new'] == "-"): return

    # Extract required data
    left = info_parser( row['INFO'])
    right = info_parser( row['INFO_R'])

    # check the number of allels
    if( not "," in row["ALT_new"]):
        # there are only two allels
        AC = str( left[0]+right[0])
        AN = str( left[1]+right[1])
    elif( "," in row['ALT'] and "," in row['ALT_R']):
        # there are three allels
        AC = str( left[0][0]+right[0][0])
        AC += "," + str( left[0][1]+right[0][1])
        AN = str( left[1][0]+right[1][0])
    else:
        # Something wrong happened
        msg = f"Error mergin INFO: {left}!={right}\n"
        msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
        msg += f"     cols:{sources}"
        raise Exception( msg)
    
    return f"AC={AC};AN={AN}"
        

# This function parses the INFO register into number related with
# AC and AN data, taking in consideration that AC can store up to
# two different values
def info_parser( INFO: str):
    # Spliting the data to get the values
    AC_AN = INFO.split( ";")
    AC_AN = [Ax.split( "=")[1] for Ax in AC_AN]
    if( not "," in AC_AN[0]):
        # for biallelic data
        return [ int(Ax) for Ax in AC_AN]
    else:
        # for triallelic data
        AC_AN[0] = AC_AN[0].split( ",")
        return [[ int(x) for x in Ax] for Ax in AC_AN]