#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


source fit_running/parser.sh $@


$TRAINING_TYPE -mc $MAIN_CATEGORY -c $CATEGORY -t $TARGET -a $ALGORITHM -rs $SLURM_ARRAY_TASK_ID -nis $N_INNER_SEARCH