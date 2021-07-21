#!/bin/bash


source fit_running/parser.sh $@


PATH_OUTPUTS=$TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY

[ -d out/$PATH_OUTPUTS ] || mkdir out/$PATH_OUTPUTS
[ -d error/$PATH_OUTPUTS ] || mkdir error/$PATH_OUTPUTS

([ ! -e out/$PATH_OUTPUTS/$ALGORITHM\_1.out ] && [ ! -e out/$PATH_OUTPUTS/$ALGORITHM\_2.out ]) || rm out/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out
([ ! -e error/$PATH_OUTPUTS/$ALGORITHM\_1.out ] && [ ! -e error/$PATH_OUTPUTS/$ALGORITHM\_2.out ]) || rm error/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out
submission_run=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_200M_00:01:00 --partition short --array=1-2 --mem-per-cpu=200M --time 00:01:00 -o out/$PATH_OUTPUTS/$ALGORITHM\_%a.out fit_running/stage/run.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< $submission_run
JOB_ID_RUN=${SPLIT_SUBMISSION_RUN[-1]}

[ ! -e out/$PATH_OUTPUTS/$ALGORITHM\manager.out ] || rm out/$PATH_OUTPUTS/$ALGORITHM\manager.out
[ ! -e error/$PATH_OUTPUTS/$ALGORITHM\manager.out ] || rm error/$PATH_OUTPUTS/$ALGORITHM\manager.out
submission_manager=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_manager --dependency=afterany:$JOB_ID_RUN -o out/$PATH_OUTPUTS/$ALGORITHM\_manager.out fit_running/stage/manager.sh -jir $JOB_ID_RUN -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_manager
