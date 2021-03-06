#!/bin/bash

TRAINING_TYPE="prediction"

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<< $PATH_CATEGORY
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)
        
        for TARGET in "age" "all" "cvd" "cancer"
        do
            ./fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a elastic_net -nis 50
            
            ./fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a light_gbm -nis 20
        done
    done
done