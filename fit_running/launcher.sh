#!/bin/bash

for TRAINING_TYPE in "basic_prediction" "prediction" "feature_importances"
do
    for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
    do
        for PATH_CATEGORY in data/$MAIN_CATEGORY/*
        do
            IFS='/' read -r a a FILE_CATEGORY <<< $PATH_CATEGORY
            CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)
            
            MAIN_CATEGORY=laboratory
            CATEGORY="Aldehydes__-__Serum__-__Special__Sample"
            if [ $TRAINING_TYPE = "basic_prediction" ]
            then
                TARGETS="all cvd cancer"
            else
                TARGETS="age all cvd cancer"
            fi 
            
            for TARGET in $TARGETS
            do
                source fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a elastic_net -nis 1
                
                source fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a light_gbm -nis 1
            done
            break
        done
        break
    done
done 