#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in ../NHANES_preprocessing/merge/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        rm out/fold_maker/$MAIN_CATEGORY/$CATEGORY.out
        sbatch -J fold_maker/$MAIN_CATEGORY/$CATEGORY -o out/fold_maker/$MAIN_CATEGORY/$CATEGORY.out fold_maker/shell_script/unit_fold_maker.sh -mc $MAIN_CATEGORY -c $CATEGORY -f 10
    done
done