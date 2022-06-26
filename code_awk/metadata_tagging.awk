# This program tags each metadata line to keep the same order after the sorting process

BEGIN {
    # Code executed at the beginning
    sort_index = 0
}

/^#/ {
    # Code to be run in each metadata line

    # Print the tagged line
    print 0 "\t" sort_index "\t" $1

    # Jump to the next line after index update
    sort_index = sort_index + 1
    next
}

{
    # Code to be run in each line if is not metadata line
    # Print the data without modifications
    print $0
}