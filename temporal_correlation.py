#!/usr/bin/env bash
#
# See https://dzone.com/articles/temporal-correlation-git for details
#

# Remove old commit log file
rm -f commit.log

# Get all commit ids from git and write it to a commit.log file
#git log --pretty='%H' > commit.log

# Get last 200 commit ids from git and write it to a commit.log file
git log --pretty='%H' | head -n 200 > commit.log

# Parse the data and generate a incidence matrix
cat commit.log | python3 temporal_correlation.py


