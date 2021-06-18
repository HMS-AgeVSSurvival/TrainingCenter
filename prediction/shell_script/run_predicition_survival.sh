#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            mkdir out/prediction/$MAIN_CATEGORY/$CATEGORY/
            
            rm out/prediction/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J prediction/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/prediction/$MAIN_CATEGORY/$CATEGORY/elastic_net.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -a elastic_net -rs 2 -nis 100
            
            rm out/prediction/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J prediction/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/prediction/$MAIN_CATEGORY/$CATEGORY/light_gbm.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -a light_gbm -rs 2 -nis 30
        done
    done
done