import sys
import argparse
import pandas as pd

from prediction import DEATH_COLUMN


def fold_maker_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Split the samples into folds according to the survival type"
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category.",
        choices=["examination", "laboratory", "questionnaire"],
        required=True,
    )
    parser.add_argument("-c", "--category", help="Name of the category.", required=True)
    parser.add_argument(
        "-f", "--number_folds", help="Number of folds.", default=10, type=int
    )

    args = parser.parse_args(argvs)
    print(args)

    fold_maker(args.main_category, args.category, args.number_folds)


def get_folds(indexes, n_folds):
    folds = pd.Series(None, index=indexes, name="fold", dtype=int)

    n_samples = len(indexes)

    n_samples_per_fold = n_samples // n_folds
    n_big_folds = n_samples % n_folds

    for fold_number in range(n_big_folds):
        folds.iloc[
            fold_number
            * (n_samples_per_fold + 1) : (fold_number + 1)
            * (n_samples_per_fold + 1)
        ] = fold_number

    for fold_number in range(n_big_folds, n_folds):
        folds.iloc[
            fold_number * n_samples_per_fold
            + n_big_folds : (fold_number + 1) * n_samples_per_fold
            + n_big_folds
        ] = fold_number

    return folds


def fold_maker(main_category, category, n_folds):
    data = pd.read_feather(
        f"../NHANES_preprocessing/merge/data/{main_category}/{category}.feather"
    ).set_index("SEQN")
    data = data.sample(frac=1, random_state=0)

    list_every_folds = []

    list_every_folds.append(get_folds(data.index[data[DEATH_COLUMN].isna()], n_folds))

    for survival_type in ["alive", "cvd", "cancer", "other"]:
        list_every_folds.append(
            get_folds(data.index[data[f"survival_type_{survival_type}"] == 1], n_folds)
        )

    data["fold"] = pd.concat(list_every_folds)

    data.reset_index().to_feather(f"data/{main_category}/{category}.feather")
