#!/bin/bash

# Check if start and end tags are provided as arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_tag> <end_tag>"
    exit 1
fi

start_tag="$1"
end_tag="$2"

# Get all tags in the repository
tags=$(git tag)

# Loop through the tags and filter the ones within the specified range
for tag in $tags; do
  if [[ "$tag" > "$start_tag" && ("$tag" < "$end_tag" || "$tag" == "$end_tag") ]]; then
        echo "$tag"
    fi
done

