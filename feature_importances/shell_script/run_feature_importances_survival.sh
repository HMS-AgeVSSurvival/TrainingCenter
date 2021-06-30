#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            mkdir out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            
            rm out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -a elastic_net -t $TARGET -rs 2 -nis 100
            
            rm out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -a light_gbm -t $TARGET -rs 2 -nis 10
        done
    done
done