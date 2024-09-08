#!/bin/bash

# Directory where the repository is located
REPO_PATH="/home/kibe/projects/test_repo"

# Change to the repository directory
cd $REPO_PATH || { echo "Repository directory not found"; exit 1; }

# Get the latest commit ID
LATEST_COMMIT=$(git rev-parse HEAD)
COMMIT_FILE="/home/kibe/projects/ci/.commit_id"

# Check if the commit ID file exists and compare
if [ ! -f $COMMIT_FILE ] || [ "$(cat $COMMIT_FILE)" != "$LATEST_COMMIT" ]; then
    echo $LATEST_COMMIT > $COMMIT_FILE
    echo "Updated .commit_id file: $LATEST_COMMIT"
else
    echo "No new commit detected."
fi
