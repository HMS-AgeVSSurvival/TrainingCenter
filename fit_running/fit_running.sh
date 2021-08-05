#!/bin/bash

source fit_running/training_parser.sh 

clear_training_arguments
parse_training_arguments $@


PATH_OUTPUTS=$TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY

if [ $TRAINING_TYPE != "basic_prediction" ]
then
    [ -d dumps/$PATH_OUTPUTS ] || mkdir -p dumps/$PATH_OUTPUTS
fi

[ -d out/$PATH_OUTPUTS ] || mkdir -p out/$PATH_OUTPUTS
[ -d error/$PATH_OUTPUTS ] || mkdir -p error/$PATH_OUTPUTS

echo -n > out/$PATH_OUTPUTS/$ALGORITHM\_1.out
echo -n > out/$PATH_OUTPUTS/$ALGORITHM\_2.out
[ ! -e error/$PATH_OUTPUTS/$ALGORITHM\_1.out ] || rm error/$PATH_OUTPUTS/$ALGORITHM\_1.out
[ ! -e error/$PATH_OUTPUTS/$ALGORITHM\_2.out ] || rm error/$PATH_OUTPUTS/$ALGORITHM\_2.out
echo -n > out/$PATH_OUTPUTS/memory_$ALGORITHM\_1.out
echo -n > out/$PATH_OUTPUTS/memory_$ALGORITHM\_2.out

submission_run=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_200M_00:01:00 --partition short --array=1-2 --mem-per-cpu=200M --time 00:01:00 -o out/$PATH_OUTPUTS/$ALGORITHM\_%a.out fit_running/stage/run.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< $submission_run
JOB_ID_RUN=${SPLIT_SUBMISSION_RUN[-1]}

echo -n > out/$PATH_OUTPUTS/$ALGORITHM\_manager.out
[ ! -e error/$PATH_OUTPUTS/$ALGORITHM\_manager.out ] || rm error/$PATH_OUTPUTS/$ALGORITHM\_manager.out
echo -n > out/$PATH_OUTPUTS/memory_$ALGORITHM\_manager.out

submission_manager=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_manager --dependency=afterany:$JOB_ID_RUN -o out/$PATH_OUTPUTS/$ALGORITHM\_manager.out fit_running/stage/manager.sh -jir $JOB_ID_RUN -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_manager
