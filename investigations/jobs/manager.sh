#!/bin/bash
#SBATCH --partition short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


DEPENDENCY_INFO=$(sacct -X -n -o state%30,Timelimit,ReqMem -j $1)

IFS=" " read -ra SPLIT_INFO <<< "$DEPENDENCY_INFO"
STATE="${SPLIT_INFO[0]}"
TIME_LIMIT="${SPLIT_INFO[1]}"
MEMORY_LIMIT="${SPLIT_INFO[2]}"

if [ $STATE == "FAILED" ]
then
    echo "The dependency has failed"

elif [ $STATE == "OUT_OF_MEMORY" ]
then
    echo "The dependency has been running out of memory: $MEMORY_LIMIT"

    # If the MEMORY_LIMIT is in megabytes
    if [[ $MEMORY_LIMIT =~ "M" ]];
    then
        memory_digits=${MEMORY_LIMIT%M*}
        if (( $(( 2 * $memory_digits )) > 1000 ));
        then 
            new_memory_digits=$(( 2 * $memory_digits / 1000 ))
            if (( $(( 2 * $memory_digits % 1000 )) > 500 ));
            then
                new_memory_digits=$(( $new_memory_digits + 1 ))
            fi
            new_memory=$new_memory_digits\G
        else
            new_memory=$(( 2 * $memory_digits ))M
        fi
    # If the MEMORY_LIMIT is in gigabytes
    elif [[ $MEMORY_LIMIT =~ "G" ]]
    then
        new_memory=$(( ${MEMORY_LIMIT%G*} + 1 ))G
    else
        echo "Weird format memory limit: $MEMORY_LIMIT"
        ## Have to exit
    fi

    echo "Rescheduling the job with more memory: $new_memory"
    
    submission_run=$(sbatch -J run_$new_memory --mem-per-cpu=$new_memory --time 00:01 -o investigations/out/run_$new_memory.out investigations/jobs/run.sh -m)
    echo $submission_run

    IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< "$submission_run"
    job_id_run="${SPLIT_SUBMISSION_RUN[-1]}"

    submission_manager=$(sbatch -J manager_$new_memory --mem-per-cpu=50M --time 00:01 --dependency=afternotok:$job_id_run -o investigations/out/manager_$new_memory.out investigations/jobs/manager.sh $job_id_run)
    echo $submission_manager

elif [ $STATE == "TIMEOUT" ]
then
    echo "The dependency has been running out of time"
    echo "Rescheduling the job with more time"
else
    echo "The dependency has been ending with an unknown state :" $STATE
fi