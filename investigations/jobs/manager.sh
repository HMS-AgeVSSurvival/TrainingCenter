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


if [ $STATE == "COMPLETED" ]
then
    echo "The job has been run successfully"
    exit

elif [ $STATE == "FAILED" ]
then
    echo "The dependency has failed"
    mv investigations/out/run_{1..2}.out investigations/error/
    mv investigations/out/manager.out investigations/error/
    exit

elif [ $STATE == "OUT_OF_MEMORY" ]
then
    echo "The dependency has been running out of memory: $MEMORY_LIMIT"
    
    # If the MEMORY_LIMIT is in megabytes
    if [[ $MEMORY_LIMIT =~ "M" ]];
    then
        memory_digits=${MEMORY_LIMIT%M*}
        # If doubling the memory makes the memory greater than a gigabyte
        if (( $(( 2 * $memory_digits )) > 1000 ));
        then 
            new_memory_digits=$(( 2 * $memory_digits / 1000 ))
            if (( $(( 2 * $memory_digits % 1000 )) > 500 ));
            then
                new_memory_digits=$(( $new_memory_digits + 1 ))
            fi
            new_memory_limit=$new_memory_digits\Gc
        else
            new_memory_limit=$(( 2 * $memory_digits ))Mc
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
    
    # If the number of hour is greater than 12 we need to change the partition
    if (( ${new_time_limit:2:0} >= 12 ));
    then
        new_partition="medium"
    else
        new_partition="short"
    fi

elif [ $STATE == "TIMEOUT" ]
then
    echo "The dependency has been running out of time: $TIME_LIMIT"

    if (( ${TIME_LIMIT:2:0} >= 10 ));
        new_time_limit=$(( ${TIME_LIMIT:2:0} + 2 )):$(( ${TIME_LIMIT:2:3} )):00
    else
        # If adding 30 minutes makes the time limit greater than an hour
        if (( ${TIME_LIMIT:2:3} + 30 > 60 ));
        then 
            new_time_limit=$(( ${TIME_LIMIT:2:0} + 1 )):$(( (${TIME_LIMIT:2:3} + 30) % 60 )):00
        else
            new_time_limit=$(( ${TIME_LIMIT:2:0} )):$(( ${TIME_LIMIT:2:3} + 30 )):00
        fi
    fi

    # If the number of hour is greater than 12 we need to change the partition
    if (( ${new_time_limit:2:0} >= 12 ));
    then
        new_partition="medium"
    else
        new_partition="short"
    fi

    echo "Rescheduling the job with more time: $new_time_limit. Same memory $MEMORY_LIMIT"
    new_memory_limit=$MEMORY_LIMIT

else
    echo "The dependency has been ending with an unknown state :" $STATE
    mv investigations/out/run_{1..2}.out investigations/error/
    mv investigations/out/manager.out investigations/error/
    exit
fi

rm investigations/out/run_{1..2}.out
submission_run=$(sbatch -J run_$new_memory_limit\_$new_time_limit --partition $new_partition --array=1-2 --mem-per-cpu=$new_memory_limit --time $new_time_limit -o investigations/out/run_%a.out investigations/jobs/run.sh -t)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< "$submission_run"
job_id_run="${SPLIT_SUBMISSION_RUN[-1]}"

rm investigations/out/manager.out
submission_manager=$(sbatch -J manager_$new_memory_limit\_$new_time_limit --mem-per-cpu=10M --time 00:01:00 --dependency=afterany:$job_id_run -o investigations/out/manager.out investigations/jobs/manager.sh $job_id_run)
echo $submission_manager