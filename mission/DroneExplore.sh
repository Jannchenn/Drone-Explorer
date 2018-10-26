#!/usr/bin/env bash

# python Parameters.py
# need to prepare all the input files: paras.txt, lambdas.txt


# roomba experiment
filename="indep_var.txt"
while read -r line
do
    para="$line"
    indep_var=(${para})
    echo ${indep_var[0]} ${indep_var[1]} >| boardinput.txt     # indep_var includes the current prob & dur_expo
    counter=1
    while [ ${counter} -le 2 ]
    do
        python Main.py --connect 127.0.0.1:14551
        ((counter++))
    done
    # Move generated reports in to new folder
    folder="${indep_var[0]}_${indep_var[1]}"  # first is probability, and second is dur_expo
    mkdir ${folder}
    mv Drone_* ${folder}
    mv Board_* ${folder}
done < "$filename"
python Avgtime.py

# move roomba folders to roomba folders
mkdir roomba
mv *_* roomba

# modify paras.txt
python Edit.py

# random experiment
filename="lambdas1.txt"
while read -r line
do
    para="$line"
    lambdas=(${para})
    echo ${lambdas[0]} ${lambdas[1]} >| boardinput.txt
    counter2=1
    while [ ${counter2} -le 2 ]
    do
        python Main.py --connect 127.0.0.1:14551
        ((counter2++))
    done
    # Move generated reports in to new folder
    folder="${lambdas[0]}_${lambdas[1]}"
    mkdir ${folder}
    mv Drone_* ${folder}
    mv Board_* ${folder}
done < "$filename"

# move random folders to random folders
mkdir random
mv *_* random

# move random, roomba to fix_buffer/fix_duration
mkdir fix_buffer #may change
mv random fix_buffer
mv roomba fix_buffer