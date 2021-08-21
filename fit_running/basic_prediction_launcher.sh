#!/bin/bash

TRAINING_TYPE="basic_prediction"

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<< $PATH_CATEGORY
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)
        
        for TARGET in "all" "cvd" "cancer"
        do
            ./fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a elastic_net -nis 1
            
            ./fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a light_gbm -nis 1
        done
    done
done