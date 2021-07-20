#!/bin/bash

for TRAINING_TYPE in "basic_prediction" "prediction" "feature_importances"
do
    for TARGET in "age" "all" "cvd" "cancer"
    do
        for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
        do
            for PATH_CATEGORY in data/$MAIN_CATEGORY/*
            do
                IFS='/' read -r a a FILE_CATEGORY <<< $PATH_CATEGORY
                CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

                if [ ! -d out/$TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
                then
                    mkdir out/TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY/
                fi
                if [ ! -d error/TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
                then
                    mkdir error/TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY/
                fi
                
                source fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a elastic_net -nis 1
                
                source fit_running/fit_running.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a light_gbm -nis 1
            done
        done
    done 
done 