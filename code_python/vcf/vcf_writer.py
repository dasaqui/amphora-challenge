#!/usr/bin/env python

# This code is to read the pandas file and export it as a compressed vcf
# 
# At this point the original metadata is lost, so I need to create new
# metadata for this file

import gzip

import pandas as pd


def vcf_writer( vcf: pd.core.frame.DataFrame, path: str):
    with gzip.open( path, 'w') as f:
        # writing headers
        f.write( b"##fileformat=VCF=4.1\n")
        f.write( b"##fileDate={datetime.now().strftime('%y%m%d')}\n")
        f.write( b"##source=meged_data\n")
        f.write( b"##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n")
        for chromosome in range(1,23):
            f.write( b"##contig=<ID=\""+str(chromosome).encode()+b"\">\n")
        f.write( b"##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count in genotypes\">\n")
        f.write( b"##INFO=<ID=AN,Number=1,Type=Integer,Description=\"Total number of alleles in called genotypes\">\n")
        f.write( b"##amphora-challenge= imported data from csv\n")
        header = b"#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT"
        for id_hash in vcf.columns[9:]:
            header += b"\t"+bytes( id_hash, "utf-8")
        f.write( header+b"\n")

        # writing data
        f.write( vcf.to_csv( header=False, index=False, sep="\t").encode())
