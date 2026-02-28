#!/bin/sh

head -n 1 ../ex02/hh_sorted.csv > hh_positions.csv

tail -n +2 "../ex02/hh_sorted.csv" | awk -F',' '
BEGIN {
    OFS=","
    patterns[0]="Junior"; patterns[1]="Middle"; patterns[2]="Senior"
}
{
    name=""
    for (ind=3;ind<=NF-2;ind++) name = name (name==""?"":",") $ind
    new_name="-"
    for(j in patterns)
        if(tolower(name) ~ tolower(patterns[j]))
            new_name = (new_name=="-"?patterns[j]:new_name "/" patterns[j])
    new_name="\""new_name"\""
    print $1,$2,new_name,$(NF-1),$NF
}
' >> hh_positions.csv
