#!/usr/bin/env bash

filename="test.txt"
while read -r line
do
    para="$line"
    indep_var=(${para})
    echo ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]}>| boardinput.txt     # indep_var includes the current prob & dur_expo & arr_rate & arr_num & die_rate
    python WriteReport.py ${indep_var[0]} ${indep_var[1]} ${indep_var[2]} ${indep_var[3]} ${indep_var[4]} "prob" "1"
done < "$filename"