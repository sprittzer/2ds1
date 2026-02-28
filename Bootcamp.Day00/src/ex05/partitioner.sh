#!/bin/sh

headers=$(head -n 1 "../ex03/hh_positions.csv")

tail -n +2 "../ex03/hh_positions.csv" | awk -F ',' -v first_line="$headers" '
{
    file_name = substr($2, 2, 10) ".csv"
    
    if (!(file_name in created_files)) {
        print first_line > file_name
        created_files[file_name] = 1
    }
    print > file_name
}'