#!/usr/bin/env python

# This code is to merge two vcf files given as pandas dataframes
#
# the output should be the merged vcf updating the corresponding
# columns (ID REF ALT FILTER INFO)
#
# because there is no data relative to QUAL this code will not
# take care of this column leaving a copy of any of the files.

from ast import If
import pandas as pd

def vcf_merge( vcf_left: pd.core.frame.DataFrame, vcf_right: pd.core.frame.DataFrame):
    # prepare the columns to merge
    columns=["ID","REF","ALT","QUAL","FILTER","INFO","FORMAT"]
    vcf_right = vcf_right.rename( columns={col:col+"_R" for col in columns})

    # merge and release memory
    vcf = pd.merge( vcf_left, vcf_right)
    del vcf_left
    del vcf_right

    # processing old columns one by one
    sources = [ src for src in vcf.columns if len(src)>8]
    vcf["ID_new"] = vcf.apply( lambda x: map_ID( x, sources), axis=1)
    vcf["REF_new"] = vcf.apply( lambda x: map_REF( x, sources), axis=1)
    vcf["ALT_new"] = vcf.apply( lambda x: map_ALT( x, sources), axis=1)
    vcf["QUAL_new"] = vcf.apply( lambda x: map_QUAL( x, sources), axis=1)
    vcf["FILTER_new"] = vcf.apply( lambda x: map_FILTER( x, sources), axis=1)
    vcf["INFO_new"] = vcf.apply( lambda x: map_INFO( x, sources), axis=1)
    vcf["FORMAT_new"] = vcf.apply( lambda x: map_FORMAT( x, sources), axis=1)

    # Deal with aditional columns
    for col in columns:
        vcf[col] = vcf[col+"_new"]
        del vcf[col+"_new"]
        del vcf[col+"_R"]
    
    # Deal with failed rows
    for col in columns:
        vcf.drop( vcf[ vcf[col] == "-"].index, inplace=True)
    
    return vcf

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

def map_FILTER( row, sources):
    # Extract required data
    left = row['FILTER']
    right = row['FILTER_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    msg = f"Error mergin ALT: {left}!={right}\n"
    msg += f"    Involved chromosome/position is {row['CHROM']}/{row['POS']}\n"
    msg += f"     cols:{sources}"
    raise Exception( msg)

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

def map_FORMAT( row, sources):
    # Extract required data
    left = row['FORMAT']
    right = row['FORMAT_R']

    # If both columns are equal return the same value
    if( left == right): return left

    # If both columns are diferent we should implement an
    # adequate function to take care of it
    raise Exception( f"error mergin FORMAT: {left}!={right}")
