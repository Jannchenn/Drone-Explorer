#!/usr/bin/env bash

# python Parameters.py
# need to prepare all the input files: paras.txt, lambdas.txt


# roomba experiment
filename="lambdas1.txt"
while read -r line
do
    para="$line"
    lambdas=(${para})
    echo ${lambdas[0]} ${lambdas[1]} ${lambdas[2]} >| boardinput.txt
    counter=1
    while [ ${counter} -le 2 ]
    do
        python Main.py --connect 127.0.0.1:14551
        ((counter++))
    done
    # Move generated reports in to new folder
    folder="${lambdas[0]}_${lambdas[1]}_${lambdas[2]}"
    mkdir ${folder}
    mv Drone_* ${folder}
    mv Board_* ${folder}
done < "$filename"
#python Avgtime.py

# move roomba folders to roomba folders
mkdir roomba
mv *_*_* roomba

## modify paras.txt
#python Edit.py
#
## random experiment
#filename="lambdas1.txt"
#while read -r line
#do
#    para="$line"
#    lambdas=(${para})
#    echo ${lambdas[0]} ${lambdas[1]} ${lambdas[2]}>| boardinput.txt
#    counter2=1
#    while [ ${counter2} -le 2 ]
#    do
#        python Main.py --connect 127.0.0.1:14551
#        ((counter2++))
#    done
#    # Move generated reports in to new folder
#    folder="${lambdas[0]}_${lambdas[1]}_${lambdas[2]}"
#    mkdir ${folder}
#    mv Drone_* ${folder}
#    mv Board_* ${folder}
#done < "$filename"
#
## move random folders to random folders
#mkdir random
#mv *_*_* random
#
## move random, roomba to fix_buffer/fix_duration
#mkdir fix_buffer #may change
#mv random fix_buffer
#mv roomba fix_buffer