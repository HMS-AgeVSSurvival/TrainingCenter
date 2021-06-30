# Interactive job
srun --partition interactive --job-name "InteractiveJob" --cpus-per-task 1 --mem-per-cpu 2G --time 2:00:00 --pty bash
module load gcc/6.2.0 python/3.7.4

# Interactive job + jupyter
srun --partition interactive --job-name "InteractiveJob" --cpus-per-task 1 --mem-per-cpu 2G --time 4:00:00 --pty --x11 --tunnel 8888:8888 bash
module load gcc/6.2.0 python/3.7.4
source env_o2/bin/activate
jupyter notebook casting/casting.ipynb --port=8888 --browser='none'