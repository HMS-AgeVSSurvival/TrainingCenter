#!/bin/bash
#SBATCH --partition short
#SBATCH --time=0-12:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu 6G
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=theo.vincent@eleves.enpc.fr

module load gcc/6.2.0
module load python/3.7.4
source env_o2/bin/activate


prediction $@