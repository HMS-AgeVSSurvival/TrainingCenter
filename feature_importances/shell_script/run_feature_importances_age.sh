#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        mkdir out/feature_importances/age/$MAIN_CATEGORY/$CATEGORY/
        
        rm out/feature_importances/age/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
        sbatch -J feature_importances/age/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/feature_importances/age/$MAIN_CATEGORY/$CATEGORY/elastic_net.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -a elastic_net -t age -rs 2 -nis 1000
        
        rm out/feature_importances/age/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
        sbatch -J feature_importances/age/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/feature_importances/age/$MAIN_CATEGORY/$CATEGORY/light_gbm.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -a light_gbm -t age -rs 2 -nis 30
    done
done