#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        for TARGET in "all" "cvd" "cancer"
        do 
            if [ ! -d out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
            then
                mkdir out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            fi
            if [ ! -d error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/ ]
            then
                mkdir error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/
            fi
            
            rm out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            rm error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out
            sbatch -J prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net -o out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out -e error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/elastic_net.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -tt full_training -t $TARGET -a elastic_net -rs 1 -nis 1 -sa
            
            rm out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            rm error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out
            sbatch -J prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm -o out/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out -e error/prediction/$TARGET/$MAIN_CATEGORY/$CATEGORY/light_gbm.out prediction/shell_script/unit_prediction.sh -mc $MAIN_CATEGORY -c $CATEGORY -tt full_training -t $TARGET -a light_gbm -rs 1 -nis 1 -sa
        done
    done
done