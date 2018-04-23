#!/usr/bin/env bash

python Parameters.py

filename="lambdas.txt"
while read -r line
do
    para="$line"
    lambdas=($para)
    echo ${lambdas[0]} ${lambdas[1]} >| boardinput.txt
    counter=1
    while [ $counter -le 5 ]
    do
        python Main.py --connect 127.0.0.1:14551
        ((counter++))
    done
    # Move generated reports in to new folder
    folder="${lambdas[0]}_${lambdas[1]}"
    mkdir $folder
    mv report* $folder
done < "$filename"
