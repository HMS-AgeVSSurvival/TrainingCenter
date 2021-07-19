#!/bin/bash


submission_run=$(sbatch -J run_200M --mem-per-cpu=200M --time 00:01 -o investigations/out/run_200M.out investigations/jobs/run.sh -m)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< "$submission_run"
job_id_run="${SPLIT_SUBMISSION_RUN[-1]}"

submission_manager=$(sbatch -J manager_200M --mem-per-cpu=50M --time 00:01 --dependency=afternotok:$job_id_run -o investigations/out/manager.out investigations/jobs/manager_200M.sh $job_id_run)
echo $submission_manager