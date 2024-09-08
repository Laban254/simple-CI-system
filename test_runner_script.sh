#!/bin/bash

# Directory where the repository is located
REPO_PATH="/home/kibe/projects/test_repo"

# Change to the repository directory
cd $REPO_PATH || { echo "Repository directory not found"; exit 1; }

# Fetch latest changes
git fetch

# Checkout the specified commit
git checkout $1

# Run your test suite here
./run_tests.sh
