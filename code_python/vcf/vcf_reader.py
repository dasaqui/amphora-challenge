#!/usr/bin/env python

# This code is to read the compressed vcf file and import it as a pandas file
# 
# the metadata will be lost in this implementation of the code.

import gzip
import io

import pandas as pd


def vcf_reader(path: str):
    with gzip.open(path, 'r') as f:
        lines = [l.decode("utf-8") for l in f if not l.startswith( b'##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})
