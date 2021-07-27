#!/bin/bash
#SBATCH --partition short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:01:00
#SBATCH --mem-per-cpu 10M

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


source fit_running/parser.sh $@


PATH_OUTPUTS=$TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY

DEPENDENCY_INFO=$(sacct -X -n -o state%30,Timelimit,ReqMem,Partition -j $JOB_ID_RUN)

IFS=" " read -ra SPLIT_INFO <<< $DEPENDENCY_INFO
STATE=${SPLIT_INFO[0]}
TIME_LIMIT=${SPLIT_INFO[1]}
MEMORY_LIMIT=${SPLIT_INFO[2]}
PARTITION=${SPLIT_INFO[3]}


if [ $STATE == "COMPLETED" ]
then
    echo "The job has been run successfully"
    exit

elif [ $STATE == "FAILED" ]
then
    echo "The dependency has failed" >&2
    mv out/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out error/$PATH_OUTPUTS/
    mv out/$PATH_OUTPUTS/$ALGORITHM\manager.out error/$PATH_OUTPUTS/
    exit

elif [ $STATE == "OUT_OF_MEMORY" ]
then
    echo "The dependency has been running out of memory: $MEMORY_LIMIT"
    
    # If the MEMORY_LIMIT is in megabytes
    if [[ $MEMORY_LIMIT =~ "M" ]];
    then
        memory_digits=${MEMORY_LIMIT%M*}
        # If doubling the memory makes the memory greater than a gigabyte
        if (( $(( 2 * $memory_digits )) < 1000 ));
        then 
            new_memory_limit=$(( 2 * $memory_digits ))Mc
        else
            new_memory_digits=$(( 2 * $memory_digits / 1000 ))
            if (( $(( 2 * $memory_digits % 1000 )) > 500 ));
            then
                new_memory_digits=$(( $new_memory_digits + 1 ))
            fi
            new_memory_limit=$new_memory_digits\Gc
        fi
    # If the MEMORY_LIMIT is in gigabytes
    elif [[ $MEMORY_LIMIT =~ "G" ]]
    then
        new_memory_limit=$(( ${MEMORY_LIMIT%G*} + 1 ))Gc
    else
        echo "Weird format memory limit: $MEMORY_LIMIT"
        exit
    fi

    echo "Rescheduling the job with more memory: $new_memory_limit. Same time limit $TIME_LIMIT"
    new_time_limit=$TIME_LIMIT
    new_partition=$PARTITION

elif [ $STATE == "TIMEOUT" ]
then
    IFS=":" read -ra SPLIT_TIME_LIMIT <<< $TIME_LIMIT
    HOURS=$(( 10#${SPLIT_TIME_LIMIT[0]} ))
    MINUTES=$(( 10#${SPLIT_TIME_LIMIT[1]} ))
    SECONDS=$(( 10#${SPLIT_TIME_LIMIT[2]} ))

    echo "The dependency has been running out of time: $TIME_LIMIT"

    if (( $HOURS < 10 ));  # Add 30 minutes
    then
        if (( $MINUTES + 30 < 60 ));
        then
            new_time_limit=$HOURS:$(( $MINUTES + 30 )):$SECONDS
        else
            new_time_limit=$(( $HOURS + 1 )):$(( ($MINUTES + 30) % 60 )):$SECONDS
        fi
    else  # Add 2 hours
        new_time_limit=$(( $HOURS + 2 )):$(( $MINUTES )):$SECONDS
    fi

    IFS=":" read -ra SPLIT_NEW_TIME_LIMIT <<< $new_time_limit
    NEW_HOURS=$(( 10#${SPLIT_NEW_TIME_LIMIT[0]} ))

    if (( $NEW_HOURS < 12 ));
    then
        new_partition="short"
    else
        new_partition="medium"
    fi

    echo "Rescheduling the job with more time: $new_time_limit. Same memory $MEMORY_LIMIT"
    new_memory_limit=$MEMORY_LIMIT

else
    echo "The dependency has been ending with an unknown state : $STATE" >&2
    mv out/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out error/$PATH_OUTPUTS/
    mv out/$PATH_OUTPUTS/$ALGORITHM\manager.out error/$PATH_OUTPUTS/
    exit
fi

rm out/$PATH_OUTPUTS/$ALGORITHM\_{1..2}.out
submission_run=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_$new_memory_limit\_$new_time_limit --partition $new_partition --array=1-2 --mem-per-cpu=$new_memory_limit --time $new_time_limit -o out/$PATH_OUTPUTS/$ALGORITHM\_%a.out fit_running/stage/run.sh -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< $submission_run
JOB_ID_RUN=${SPLIT_SUBMISSION_RUN[-1]}

rm out/$PATH_OUTPUTS/$ALGORITHM\_manager.out
submission_manager=$(sbatch -J $PATH_OUTPUTS/$ALGORITHM\_manager --dependency=afterany:$JOB_ID_RUN -o out/$PATH_OUTPUTS/$ALGORITHM\_manager.out fit_running/stage/manager.sh -jir $JOB_ID_RUN -tt $TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -nis $N_INNER_SEARCH)
echo $submission_manager