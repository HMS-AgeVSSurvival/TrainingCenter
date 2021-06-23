#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            mkdir out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            
            rm out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -a elastic_net -t $TARGET -rs 2 -nis 1000
            
            rm out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -a light_gbm -t $TARGET -rs 2 -nis 10
        done
    done
done