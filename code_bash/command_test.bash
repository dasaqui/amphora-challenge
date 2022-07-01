#!/bin/bash

# If the command exist inform it
command -v $1 && \
echo "$2 installed correctly"

# If the program doesn't exist tell the user
command -v $1 >/dev/null || \
echo "$2 is not installed and we need it, please install it"

# exit with error if the command can't be found
echo ""
command -v $1 >/dev/null || exit 1