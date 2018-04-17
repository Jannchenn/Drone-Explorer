#!/bin/bash

python Parameters.py

filename="lambdas.txt"
while read -r line
do
    para="$line"
    lambdas=($para)
    echo ${lambdas[0]} ${lambdas[1]} >| boardinput.txt
    python Main.py --connect 127.0.0.1:14551
    # Move generated reports in to new folder
    folder="${lambdas[0]}_${lambdas[1]}"
    mkdir $folder
    mv report* $folder
done < "$filename"
