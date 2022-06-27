# This code is to convert a csv file into a vcf file
#
# this code will split the output in metadata file and
# chromosomes to be sorted later

BEGIN {
    # Printing all the metadata 
    print "##fileformat=VCFv4.1" > output
    print "##filedate="meta > output
    print "##source="id_hash".csv" > output
    print "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">" > output
    for (chromosome = 1; chromosome < 23; chromosome++)
        print "##contig=<ID="chromosome">" > output
    print "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count in genotypes\">" > output
    print "##INFO=<ID=AN,Number=1,Type=Integer,Description=\"Total number of alleles in called genotypes\">" > output
    print "##amphora-challenge: imported data from csv" > output
    print "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	"id_hash > output
}

# ignore the header of the input file
/,REF,/ { next}

# check for bialellic SNPs
$4 == $5 {
    REF=$3
    ALT=$4
}

# check for trialellic SNPs
$4 == $5 {
    REF=$3
    ALT=$4","$5
}

# split by chromosome
{
    CHROM=$1

}