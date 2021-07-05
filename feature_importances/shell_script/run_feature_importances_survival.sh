#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            if [ ! -d out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
            then
                mkdir out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            fi
            if [ ! -d error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
            then
                mkdir error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            fi
            
            rm out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            rm error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out -e error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a elastic_net -rs 2 -nis 1 -sa
            
            rm out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            rm error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out -e error/feature_importances/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out feature_importances/shell_script/unit_feature_importances.sh -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a light_gbm -rs 2 -nis 1 -sa
        done
    done
done