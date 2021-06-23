import argparse
import sys

import pandas as pd
import numpy as np


def feature_importances_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to train and output the feature importances from the datasets"
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
        "-a",
        "--algorithm",
        help="The name of the algorithm.",
        choices=["elastic_net", "light_gbm"],
        required=True,
    )
    parser.add_argument(
        "-t",
        "--target",
        help="The target of the algorithm.",
        choices=["age", "all", "cvd", "cancer"],
        required=True,
    )
    parser.add_argument(
        "-rs",
        "--random_state",
        type=int,
        help="Random state during the training.",
        choices=[1, 2],
        required=True,
    )
    parser.add_argument(
        "-nis",
        "--n_inner_search",
        default=1,
        type=int,
        help="The number of evaluation in the hyperparameters space",
    )

    args = parser.parse_args(argvs)
    print(args)

    if args.target == "age":
        feature_importances_age(
            args.main_category,
            args.category,
            args.algorithm,
            args.random_state,
            args.n_inner_search,
        )
    else:
        feature_importances_survival(
            args.main_category,
            args.category,
            args.algorithm,
            args.target,
            args.random_state,
            args.n_inner_search,
        )


def feature_importances_age(main_category, category, algorithm, random_state, n_inner_search):
    from sklearn.metrics import r2_score, mean_squared_error

    from prediction.model import ModelAge
    from prediction.scale import scale_age
    from prediction.inner_cross_validation import inner_cross_validation_age
    from feature_importances.utils import update_results_age
    from prediction import AGE_COLUMN

    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    model = ModelAge(algorithm, random_state)

    train_set = data.sample(frac=1, random_state=0)

    hyperparameters = inner_cross_validation_age(
        train_set, algorithm, random_state, n_inner_search
    )

    model.set(**hyperparameters)

    scaled_train_set, age_mean, age_std = scale_age(train_set)

    model.fit(scaled_train_set)
    
    train_prediction = model.predict(scaled_train_set) * age_std + age_mean

    train_r2 = r2_score(
            train_set.loc[train_prediction.index, AGE_COLUMN], train_prediction
    )
    train_rmse = mean_squared_error(
            train_set.loc[train_prediction.index, AGE_COLUMN],
            train_prediction,
            squared=False,
    ).astype(np.float64)

    metrics = {"train r²": train_r2, "train RMSE": train_rmse}

    update_results_age(main_category, category, algorithm, metrics)


def feature_importances_survival(main_category, category, algorithm, target, random_state, n_inner_search):
    from sksurv.metrics import concordance_index_censored

    from prediction.model import ModelSurvival
    from prediction.scale import scale_survival
    from prediction.inner_cross_validation import inner_cross_validation_survival
    from feature_importances.utils import update_results_survival
    from prediction import DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN

    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    model = ModelSurvival(algorithm, random_state)

    if target == "all":
        data.drop(index=data.index[data["survival_type_alive"].isna()], inplace=True)
    elif target == "cvd":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cvd"] == 1)]
    elif target == "cancer":
        data = data[(data["survival_type_alive"] == 1) | (data["survival_type_cancer"] == 1)]

    if (not data.empty) and (data[DEATH_COLUMN].sum() > len(data["fold"].drop_duplicates())):
        train_set = data.sample(frac=1, random_state=0)

        hyperparameters = inner_cross_validation_survival(
            train_set, algorithm, random_state, n_inner_search
        )

        model.set(**hyperparameters)

        scaled_train_set = scale_survival(train_set)

        model.fit(scaled_train_set)

        train_prediction = model.predict(scaled_train_set)

        train_c_index = concordance_index_censored(train_set.loc[train_prediction.index, DEATH_COLUMN].astype(bool), train_set.loc[train_prediction.index, FOLLOW_UP_TIME_COLUMN], train_prediction)[0]
             
        metrics = {"train C-index": train_c_index}

        update_results_survival(main_category, category, algorithm, target, metrics)

    else:
        metrics = {"train C-index": -1}

        update_results_survival(main_category, category, algorithm, target, metrics)
