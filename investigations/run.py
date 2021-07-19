import argparse
import sys
import time
import pandas as pd
from tqdm import tqdm


time.sleep(10)
argvs=sys.argv[1:]

parser = argparse.ArgumentParser(
    "Pipeline to train and output the predictions from the datasets"
)
parser.add_argument(
    "-f", "--fail", help="Fail the job", action="store_true", default=False
)
parser.add_argument(
    "-m", "--memory", help="Make the job lacking of memory", action="store_true", default=False
)
parser.add_argument(
    "-t", "--time", help="Make the job time out", action="store_true", default=False
)
parser.add_argument(
    "-rs",
    "--random_state",
    type=int,
    help="Random state during the training.",
    choices=[1, 2],
    required=True,
)


args = parser.parse_args(argvs)
print(args)

print("Random state :", args.random_state)

if args.fail:
    1 / 0
if args.memory:
    endless_list = []
    for i in tqdm(range(10)):
        endless_list.append(pd.read_feather("data/examination/Oral__Health__-__Dentition.feather"))
if args.time:
    time.sleep(61)


