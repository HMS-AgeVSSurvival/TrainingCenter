#!/bin/bash


function echo_new_launch() {
    echo ""
    echo ""
    echo "new_time_limit : $new_time_limit"
    echo "new_memory_limit : $new_memory_limit"
    echo "new_partition : $new_partition"
    echo "new_n_inner_search : $new_n_inner_search"
    echo ""
    echo ""
}


function launch_manager() {
    local IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< $submission_run
    local JOB_ID_RUN=${SPLIT_SUBMISSION_RUN[-1]}

    echo_new_launch >> out/$PATH_OUTPUTS/$ALGORITHM\_manager.out
    local submission_manager=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_manager --dependency=afterany:$JOB_ID_RUN -o out/$PATH_OUTPUTS/$ALGORITHM\_manager.out fit_running/stage/manager.sh -jir $JOB_ID_RUN -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $new_n_inner_search)
    echo $submission_manager
}


function launch_array() {
    echo_new_launch >> out/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out
    local submission_run=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_$new_memory_limit\_$new_time_limit --partition $new_partition --array=1-2 --mem-per-cpu=$new_memory_limit --time $new_time_limit -o out/$PATH_OUTPUTS/$ALGORITHM\_%a.out fit_running/stage/run.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $new_n_inner_search)
    echo $submission_run

    launch_manager
}


function launch_job() {
    RANDOM_STATE=$1

    echo_new_launch >> out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out
    local submission_run=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_$new_memory_limit\_$new_time_limit --partition $new_partition --array=$RANDOM_STATE --mem-per-cpu=$new_memory_limit --time $new_time_limit -o out/$PATH_OUTPUTS/$ALGORITHM\_%a.out fit_running/stage/run.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $new_n_inner_search)
    echo $submission_run

    launch_manager
}