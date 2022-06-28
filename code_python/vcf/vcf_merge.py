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

from .merge_mapping import *


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
