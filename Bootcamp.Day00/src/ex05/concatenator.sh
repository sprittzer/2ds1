#!/bin/sh

files=$(ls *.csv)
file1_header=$(echo "$files" | head -n 1)

head -n 1 "$file1_header" > hh_positions.csv
for file in $files; do
    tail -n +2 "$file" >> hh_positions.csv
done