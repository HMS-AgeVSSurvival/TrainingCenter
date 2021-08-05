#!/bin/bash
#SBATCH --partition short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:01:00
#SBATCH --mem-per-cpu 10M

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


source fit_running/training_parser.sh 

clear_training_arguments
parse_training_arguments $@

PATH_OUTPUTS=$TRAINING_TYPE/$TARGET/$MAIN_CATEGORY/$CATEGORY


DEPENDENCY_INFO=$(sacct -X -n -o state%30,Timelimit,ReqMem,Partition -j $JOB_ID_RUN)

local IFS=" " read -ra SPLIT_INFO <<< $DEPENDENCY_INFO
STATE_1=${SPLIT_INFO[0]}
TIME_LIMIT=${SPLIT_INFO[1]}
MEMORY_LIMIT=${SPLIT_INFO[2]}
PARTITION=${SPLIT_INFO[3]}
STATE_2=${SPLIT_INFO[4]}


source fit_running/stage/understand_state.sh

RELAUNCH_1=true
RELAUNCH_2=true

check_if_relaunch 1
RELAUNCH_1=$RELAUNCH
check_if_relaunch 2
RELAUNCH_2=$RELAUNCH

new_time_limit=$TIME_LIMIT
new_memory_limit=$MEMORY_LIMIT
new_partition=$PARTITION
new_n_inner_search=$N_INNER_SEARCH

update_requirements

source fit_running/stage/job_launcher.sh

if [ $RELAUNCH_1 && $RELAUNCH_2 ]
then
    launch_array
elif [ $RELAUNCH_1 ]
    launch_job 1
elif [ $RELAUNCH_2 ]
    launch_job 2