#!/bin/bash

function decompose_time() {
    local IFS=":" read -ra SPLIT_TIME_LIMIT <<< $1
    $2["hour"]=$(( 10#${SPLIT_TIME_LIMIT[0]} ))
    $2["minutes"]=$(( 10#${SPLIT_TIME_LIMIT[1]} ))
    $2["seconds"]=$(( 10#${SPLIT_TIME_LIMIT[2]} ))
}


function compute_max_time() {
    if (( $1["hour"]$1["minutes"]$1["seconds] > $2["hour"]$2["minutes"]$2["seconds] ))
    then
        MAX_TIME=$TIME_1
    else 
        MAX_TIME=$TIME_2
    fi
}  


function set_max_time() {
    local TIME_1=$1
    local TIME_2=$2

    local declare -A time_decomposition_1=( ["hour"]="" ["minutes"]="" ["seconds"]="" )
    local declare -A time_decomposition_2=( ["hour"]="" ["minutes"]="" ["seconds"]="" )

    decompose_time TIME_1 time_decomposition_1
    decompose_time TIME_2 time_decomposition_2
    
    compute_max_time time_decomposition_1 time_decomposition_2
}