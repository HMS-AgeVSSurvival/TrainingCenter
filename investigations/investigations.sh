#!/bin/bash

out/prediction/age/$MAIN_CATEGORY/$CATEGORY/elastic_net
rm investigations/out/run_{1..2}.out
rm investigations/error/run_{1..2}.out
submission_run=$(sbatch -J run_200M_00:01:00 --partition short --array=1-2 --mem-per-cpu=200M --time 00:01:00 -o investigations/out/run_%a.out investigations/jobs/run.sh -t)
echo $submission_run

IFS=" " read -ra SPLIT_SUBMISSION_RUN <<< "$submission_run"
job_id_run="${SPLIT_SUBMISSION_RUN[-1]}"

rm investigations/out/manager.out
rm investigations/error/manager.out
submission_manager=$(sbatch -J manager_200M_00:01:00 --mem-per-cpu=10M --time 00:01:00 --dependency=afterany:$job_id_run -o investigations/out/manager.out investigations/jobs/manager.sh $job_id_run)
echo $submission_manager