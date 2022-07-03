# This code is to receive the merged data and get a new sample file
#
# The sample file contains all the information of the input vcf
# removing all the samples to put an empty sample that will preserve
# the required data to make predictions

BEGIN{
    OFS = FS

    sample_hash = "sample"
    empty_data = "."
    INFO_1 = "AC=0;AN=0"
    INFO_2 = "AC=0,0;AN=0"
}

NF == 1 {
    # To print all the metadata
    print $0
    next
}

NF > 9 && $1 == "#CHROM" {
    # To print the correct headers
    $10 = sample_hash
    print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10
    next
}

NF > 9 && $5 ~ "," {
    # To print data rows on triallelic data
    $8 = INFO_2
    $10 = empty_data
    print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10
    next
}

NF > 9 {
    # To print data rows on biallelic data
    $8 = INFO_1
    $10 = empty_data
    print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10
}
