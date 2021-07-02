#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            if [ ! -d out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
            then
                mkdir out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            fi
            
            rm out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -tt basic_training -t $TARGET -a elastic_net -rs 2 -nis 1
            
            rm out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/basic_prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -tt basic_training -t $TARGET -a light_gbm -rs 2 -nis 1
        done
    done
done