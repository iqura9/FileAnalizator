#!/bin/bash

read -p "Enter the directory path: " dir_path

find "$dir_path" -type f -exec ls -l {} + | grep -v '^total' | awk '{print $5}' > file_sizes.txt

echo "File sizes have been saved to file_sizes.txt"

python3 main.py