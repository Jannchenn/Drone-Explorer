#!/usr/bin/env bash

    # set up file of aggregated reports for Graph
    # put all merged files into one directory
    awk 'FNR==1 && NR!=1 {next;}{print}' Drone_Total*.csv > random_fixed_buffer_merged.csv
    awk 'FNR==1 && NR!=1 {next;}{print}' Drone_Total*.csv > roomba_fixed_buffer_merged.csv

    # provide Graph with argument for X axis label (lambda buffer or duration)
    x_label = "Lambda Duration (sec)"
    random_merged_file = "'random_fixed_buffer_merged.csv'"
    roomba_merged_file = "'roomba_fixed_buffer_merged.csv'"

    python Graph.py "$x_label" "$random_merged_file" "$roomba_merged_file"

    # set up file of aggregated reports for Graph
    # put all merged files into one directory
    awk 'FNR==1 && NR!=1 {next;}{print}' Drone_Total*.csv > random_fixed_duration_merged.csv
    awk 'FNR==1 && NR!=1 {next;}{print}' Drone_Total*.csv > roomba_fixed_duration_merged.csv

    # provide Graph with argument for X axis label (lambda buffer or duration)
    x_label = "Lambda Duration (sec)"
    random_merged_file = "'random_fixed_duration_merged.csv'"
    roomba_merged_file = "'roomba_fixed_duration_merged.csv'"

    python Graph.py "$x_label" "$random_merged_file" "$roomba_merged_file"
