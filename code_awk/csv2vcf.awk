# This code is to convert a csv file into a vcf file
#
# this code will split the output in metadata file and
# chromosomes to be sorted later

BEGIN {
    # Configuring all the separators
    FS = ","
    OFS = "\t"

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
NR == 1 { next}

# check for bialellic SNPs
$4 == $5 {
    REF = $3
    ALT = $4
}

# check for trialellic SNPs
$4 != $5 {
    REF = $3
    ALT = $4","$5
}

# split by chromosome
{
    CHROM = $1
    POS = $2
    ID = $3
    QUAL = "." 

    # facts
    # I will supose that each filter was passed
    # I will supose that the genotype is phased
    # With my current knowledge and only one file i can't 
    #    reconstruct the original genome to determine the
    #    correct SNP for each row
    FILTER = "PASS"
    gsub( /\"/, "", $6)
    gsub( /\"/, "", $7)
    AC = $6 + $7

    # Data sorting
    $10 = $6"|"$7       # Hash
    $9 = "GT"           # FORMAT
    $8 = "AC="AC";AN=2" # INFO
    $7 = "PASS"         # FILTER
    $6 = "."            # QUAL
    $5 = ALT            # ALT
    $4 = REF            # REF
    $3 = "."            # ID
    $2 = POS            # POS
    $1 = CHROM          # CHROM

    # Print current row splitting the output by chromosome
    print $0 > output"_"CHROM
}