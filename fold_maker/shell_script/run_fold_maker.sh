#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    [ -d out/fold_maker/$MAIN_CATEGORY ] || mkdir -p out/fold_maker/$MAIN_CATEGORY
    [ -d error/fold_maker/$MAIN_CATEGORY ] || mkdir -p error/fold_maker/$MAIN_CATEGORY
    
    for PATH_CATEGORY in ../NHANES_preprocessing/merge/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        echo -n > out/fold_maker/$MAIN_CATEGORY/$CATEGORY.out
        echo -n > error/fold_maker/$MAIN_CATEGORY/$CATEGORY.out

        sbatch -J fold_maker/$MAIN_CATEGORY/$CATEGORY -o out/fold_maker/$MAIN_CATEGORY/$CATEGORY.out -e error/fold_maker/$MAIN_CATEGORY/$CATEGORY.out fold_maker/shell_script/unit_fold_maker.sh -mc $MAIN_CATEGORY -c $CATEGORY -f 10
    done
done